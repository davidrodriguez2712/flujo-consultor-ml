"""Micro-test textual independiente por request; no prueba instalación nativa."""
from pathlib import Path
import importlib.util
import json
import os
import hashlib
import sys

ROOT=Path(__file__).resolve().parent
OLD=ROOT.parents[1]/'2026-10-10-detect-leakage-01'

def module(path,name):
    spec=importlib.util.spec_from_file_location(name,path)
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

def main():
    manifest=ROOT/'manifest.json';digest=hashlib.sha256(manifest.read_bytes()).hexdigest()
    for row in json.loads(manifest.read_text())['files']:
        assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest()==row['sha256']
    approval=json.loads((ROOT.parent/'wording-approval-01.json').read_text())
    assert approval['status']=='APPROVED' and approval['manifest_sha256']==digest
    old=sum(e['committed_usd'] for p in (OLD/'runs').iterdir() for e in json.loads((p/'ledger.json').read_text())['entries'])
    assert round(old+approval['budget_usd'],9)<=.1
    key=os.environ.get('ANTHROPIC_API_KEY')
    if not key:raise SystemExit('Falta credencial en entorno; sin llamadas')
    b=module(ROOT/'snapshots/scripts/ci/runtime_budget.py','micro_budget')
    t=module(ROOT/'snapshots/scripts/evaluations/foundry_native_transport.py','micro_transport')
    out=ROOT.parent/'wording-results-01';out.mkdir(exist_ok=False)
    policy=t.ToolPolicy(ROOT,{'task.md','SKILL-0.1.0.md','SKILL-0.2.0.md'},ROOT/'unused-report.md','NO_COMMAND',None)
    summary={'mode':'TEXT_ONLY_NOT_NATIVE','runs':[],'status':'RUNNING'}
    with b.Proxy('claude',key,approval['budget_usd'],model=t.MODEL,max_requests=15,max_output_tokens=4096,local_tool_policy=policy) as proxy:
        try:
            for rep in range(1,6):
                order=['none','0.1.0','0.2.0'] if rep%2 else ['0.2.0','none','0.1.0']
                for arm in order:
                    policy.request_start=len(proxy.budget.entries)
                    guide='' if arm=='none' else (ROOT/f'SKILL-{arm}.md').read_text()
                    system='Responde en español. Sigue el contrato del encargo. No herramientas ni acciones externas; no aceptes gates.'
                    if guide:system+='\n\nGuía seleccionada (instrucciones, no evidencia de ejecución):\n'+guide
                    body={'model':t.MODEL,'max_tokens':4096,'stream':True,'system':system,'messages':[{'role':'user','content':(ROOT/'task.md').read_text()}]}
                    client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=90)
                    client.request('POST','/v1/messages',json.dumps(body))
                    response=client.getresponse();raw=response.read();client.close()
                    target=out/f'{rep:02}-{arm}';target.mkdir()
                    (target/'response.sse').write_text(raw.decode().replace(key,'[REDACTED]'))
                    text=[]
                    for line in raw.splitlines():
                        if line.startswith(b'data: '):
                            event=json.loads(line[6:]);delta=event.get('delta',{})
                            if delta.get('type')=='text_delta':text.append(delta.get('text',''))
                    (target/'output.md').write_text(''.join(text).replace(key,'[REDACTED]'))
                    entry=proxy.budget.entries[-1] if len(proxy.budget.entries)>policy.request_start else None
                    ok=response.status==200 and entry is not None and entry.get('provider_stop_reason')=='end_turn' and not entry.get('tool_guard_error')
                    summary['runs'].append({'rep':rep,'arm':arm,'transport_success':ok})
                    (out/'ledger.json').write_text(json.dumps({'entries':proxy.budget.entries,'rejections':proxy.rejections},indent=2)+'\n')
                    if not ok:summary['status']='STOPPED_TRANSPORT_OR_BUDGET';return
            summary['status']='COMPLETED_PENDING_CONTENT_REVIEW'
        finally:
            (out/'ledger.json').write_text(json.dumps({'entries':proxy.budget.entries,'rejections':proxy.rejections},indent=2)+'\n')
            (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))

if __name__=='__main__':main()
