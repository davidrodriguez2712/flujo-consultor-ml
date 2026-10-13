"""Comparación textual, una request fresca por muestra; no runtime nativo."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import importlib.util
import json
import os

ROOT = Path(__file__).resolve().parent


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def main():
    manifest = ROOT/'manifest.json'
    digest = hashlib.sha256(manifest.read_bytes()).hexdigest()
    for row in json.loads(manifest.read_text())['files']:
        assert hashlib.sha256((ROOT/row['path']).read_bytes()).hexdigest() == row['sha256']
    approval = json.loads((ROOT.parent/'micro-approval.json').read_text())
    assert approval['status'] == 'APPROVED' and approval['manifest_sha256'] == digest
    prior = 0
    for row in json.loads((ROOT/'prior-ledgers.json').read_text()):
        path = Path(row['path'])
        assert hashlib.sha256(path.read_bytes()).hexdigest() == row['sha256']
        entries = json.loads(path.read_text())['entries']
        assert all(e.get('estimated_usd') is not None for e in entries)
        prior += sum(e['committed_usd'] for e in entries)
    assert abs(prior-approval['prior_usd']) < 1e-10
    assert prior+approval['budget_usd'] <= .15
    out = ROOT.parent/'micro-results-01'
    assert not out.exists()
    key = os.environ.get('ANTHROPIC_API_KEY')
    assert key, 'Credencial ausente'
    budget = module(ROOT/'snapshots/scripts/ci/runtime_budget.py', 'v021_micro_budget')
    transport = module(ROOT/'snapshots/scripts/evaluations/foundry_native_transport.py', 'v021_micro_transport')
    policy = transport.ToolPolicy(ROOT, {'task.md','SKILL-0.2.0.md','SKILL-0.2.1.md'},
                                  ROOT/'unused-report.md', 'NO_COMMAND', None)
    out.mkdir()
    summary = {'mode':'TEXT_ONLY_NOT_NATIVE','runs':[], 'status':'RUNNING'}
    with budget.Proxy('claude',key,approval['budget_usd'],model=transport.MODEL,
                      max_requests=10,max_output_tokens=3072,local_tool_policy=policy) as proxy:
        try:
            for rep in range(1,6):
                for arm in (['0.2.0','0.2.1'] if rep%2 else ['0.2.1','0.2.0']):
                    policy.request_start = len(proxy.budget.entries)
                    system = ('Responde en español. Sin herramientas, acciones externas ni gates. '
                              'Guía textual, no instalada/invocada nativamente. '
                              'Versión seleccionada: '+arm+'. Fecha real de ejecución: '
                              +datetime.now(timezone.utc).date().isoformat()+'.\n\n'
                              +(ROOT/f'SKILL-{arm}.md').read_text())
                    body={'model':transport.MODEL,'max_tokens':3072,'stream':True,'system':system,
                          'messages':[{'role':'user','content':(ROOT/'task.md').read_text()}]}
                    client=budget.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=120)
                    client.request('POST','/v1/messages',json.dumps(body))
                    response=client.getresponse();raw=response.read();client.close()
                    target=out/f'{rep:02}-{arm}';target.mkdir()
                    (target/'response.sse').write_text(raw.decode().replace(key,'[REDACTED]'))
                    texts=[]
                    for line in raw.splitlines():
                        if line.startswith(b'data: '):
                            delta=json.loads(line[6:]).get('delta',{})
                            if delta.get('type')=='text_delta':texts.append(delta.get('text',''))
                    (target/'output.md').write_text(''.join(texts).replace(key,'[REDACTED]'))
                    entry=proxy.budget.entries[-1] if len(proxy.budget.entries)>policy.request_start else None
                    ok=(response.status==200 and entry is not None
                        and entry.get('provider_stop_reason')=='end_turn'
                        and not entry.get('tool_guard_error') and entry.get('estimated_usd') is not None)
                    summary['runs'].append({'rep':rep,'arm':arm,'transport_success':ok})
                    (out/'ledger.json').write_text(json.dumps({'entries':proxy.budget.entries,'rejections':proxy.rejections},indent=2)+'\n')
                    if not ok:
                        summary['status']='STOPPED_TRANSPORT_OR_BUDGET'
                        return
            summary['status']='COMPLETED_PENDING_CONTENT_REVIEW'
        finally:
            proxy.budget.max_requests=len(proxy.budget.entries)
            (out/'ledger.json').write_text(json.dumps({'entries':proxy.budget.entries,'rejections':proxy.rejections},indent=2)+'\n')
            (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary))


if __name__=='__main__':
    main()
