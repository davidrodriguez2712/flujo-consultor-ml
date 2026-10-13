"""Controles del transporte Foundry, sin claves ni proveedores reales."""
import importlib.util
import json
from pathlib import Path
import pytest


def module():
    path=Path(__file__).parents[1]/'scripts/evaluations/foundry_native_transport.py'
    spec=importlib.util.spec_from_file_location('foundry_native_transport',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def policy(tmp_path):
    m=module();root=tmp_path/'work';root.mkdir();(root/'inputs').mkdir()
    (root/'case.md').write_text('public');(root/'inputs/data.csv').write_text('x\n1\n')
    return m,m.ToolPolicy(root,{'case.md','inputs/data.csv'},root/'reports/leakage/audit.md',
                           'python fixed-check.py',None)


def test_policy_limits_read_write_and_fixed_command(tmp_path):
    m,p=policy(tmp_path)
    p.validate_tool_call('Read',{'file_path':str(p.root/'inputs/data.csv')})
    p.validate_tool_call('Bash',{'command':'python fixed-check.py'})
    for name,args in [('Read',{'file_path':str(tmp_path/'expected.md')}),
                      ('Write',{'file_path':str(p.root/'inputs/data.csv'),'content':'overwrite'}),
                      ('Bash',{'command':'python fixed-check.py; cat ../expected.md'}),
                      ('Skill',{'skill':'other'}),('Agent',{})]:
        with pytest.raises(ValueError):p.validate_tool_call(name,args)
    p.validate_tool_call('Write',{'file_path':str(p.report),'content':'new report'})
    with pytest.raises(ValueError):p.validate_tool_call('Write',{'file_path':str(p.report),'content':'overwrite'})


def test_policy_rejects_symlink_and_input_mutation(tmp_path):
    m,p=policy(tmp_path);outside=tmp_path/'secret';outside.write_text('private')
    (p.root/'inputs/data.csv').unlink();(p.root/'inputs/data.csv').symlink_to(outside)
    with pytest.raises(ValueError):p.validate_tool_call('Read',{'file_path':str(p.root/'inputs/data.csv')})


def test_skill_event_requires_exact_installed_name(tmp_path):
    m,p=policy(tmp_path);p.skill='acos-eval:detect-leakage'
    p.validate_tool_call('Skill',{'skill':'acos-eval:detect-leakage'})
    with pytest.raises(ValueError):p.validate_tool_call('Skill',{'skill':'detect-leakage'})


def test_guard_assembles_split_tool_input_before_allowing_delivery(tmp_path):
    m,p=policy(tmp_path)
    events=[{'type':'content_block_start','index':0,'content_block':{'type':'tool_use','id':'t1','name':'Read','input':{}}},
            {'type':'content_block_delta','index':0,'delta':{'type':'input_json_delta','partial_json':'{"file_path":'}},
            {'type':'content_block_delta','index':0,'delta':{'type':'input_json_delta','partial_json':json.dumps(str(tmp_path/'expected.md'))+'}'}},
            {'type':'content_block_stop','index':0}]
    with pytest.raises(ValueError):m.validate_provider_tools(events,p)
    assert not p.tool_calls


def test_workspace_copies_only_public_inputs_and_exact_skill(tmp_path):
    m=module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('public');(case/'inputs/data.csv').write_text('a\n1\n')
    (case/'expected.md').write_text('PRIVATE');skill=tmp_path/'SKILL.md';skill.write_text('---\nname: detect-leakage\nversion: 0.2.0\n---\nskill bytes')
    workspace=tmp_path/'workspace'
    plugin=m.stage_workspace(case,workspace,skill)
    assert not (workspace/'expected.md').exists()
    assert (plugin/'skills/detect-leakage/SKILL.md').read_bytes()==skill.read_bytes()
    assert (workspace/'inputs/data.csv').read_bytes()==(case/'inputs/data.csv').read_bytes()
    assert json.loads((plugin/'.claude-plugin/plugin.json').read_text())['version']=='0.2.0'
    context=json.loads((workspace/'.runtime/report-context.json').read_text())
    assert context['condicion']=='treatment' and context['version']=='0.2.0'
    assert context['skill_sha256']==m.digest(skill)
    with pytest.raises(FileExistsError):m.stage_workspace(case,workspace,skill)


def test_workspace_preserves_common_workflow_snapshot(tmp_path):
    m=module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('public');workflow=tmp_path/'workflow.md'
    workflow.write_text('Shared frozen OS workflow')
    workspace=tmp_path/'workspace'
    m.stage_workspace(case,workspace,workflow=workflow)
    assert (workspace/'workflow.md').read_bytes()==workflow.read_bytes()


def budget_module():
    path=Path(__file__).parents[1]/'scripts/ci/runtime_budget.py'
    spec=importlib.util.spec_from_file_location('foundry_budget_test',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def sse(model, content, reason):
    message={'id':'msg_local','type':'message','role':'assistant','model':model,'content':[],
             'stop_reason':None,'stop_sequence':None,'usage':{'input_tokens':30,'output_tokens':0}}
    events=[{'type':'message_start','message':message}]
    for i,block in enumerate(content):
        initial=dict(block)
        if block['type']=='tool_use':
            initial['input']={}
            delta={'type':'input_json_delta','partial_json':json.dumps(block['input'])}
        else:
            initial['text']=''
            delta={'type':'text_delta','text':block['text']}
        events.append({'type':'content_block_start','index':i,'content_block':initial})
        events.append({'type':'content_block_delta','index':i,'delta':delta})
        events.append({'type':'content_block_stop','index':i})
    events += [{'type':'message_delta','delta':{'stop_reason':reason,'stop_sequence':None},'usage':{'output_tokens':30}}, {'type':'message_stop'}]
    return b''.join(('event: '+e['type']+'\ndata: '+json.dumps(e)+'\n\n').encode() for e in events)


def fake_upstream(m,monkeypatch,sequence):
    import io
    requests=[]
    class Response:
        status=200
        def __init__(self,data):self.data=io.BytesIO(data)
        def getheader(self,*args):return 'text/event-stream'
        def readline(self):return self.data.readline()
    class Connection:
        def __init__(self,*args,**kwargs):pass
        def request(self,method,path,body,headers):requests.append(json.loads(body))
        def getresponse(self):return Response(sequence.pop(0))
        def close(self):pass
    monkeypatch.setattr(m.http.client,'HTTPSConnection',Connection)
    return requests


def test_proxy_rejects_provider_model_before_delivering_tool(tmp_path,monkeypatch):
    m,p=policy(tmp_path);b=budget_module()
    payload=sse('different-model',[{'type':'tool_use','id':'t','name':'Write','input':{'file_path':str(p.report),'content':'no'}}],'tool_use')
    payload=payload.replace(b'"output_tokens": 30',b'"output_tokens": 30, "input_tokens": 30')
    fake_upstream(b,monkeypatch,[payload])
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,local_tool_policy=p) as proxy:
        client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=5)
        client.request('POST','/v1/messages',json.dumps({'model':m.MODEL,'max_tokens':100}))
        result=client.getresponse().read();client.close()
        assert b'"type": "error"' in result and b'content_block_stop' not in result
        assert proxy.budget.entries[0].get('tool_guard_error')
        assert not p.tool_calls


def test_proxy_unknown_usage_never_delivers_tool_and_stops_requests(tmp_path,monkeypatch):
    m,p=policy(tmp_path);b=budget_module()
    payload=sse(m.MODEL,[{'type':'tool_use','id':'t','name':'Read','input':{'file_path':str(p.root/'case.md')}}],'tool_use')
    payload=payload.replace(b'"input_tokens": 30',b'"cache_read_input_tokens": 30')
    requests=fake_upstream(b,monkeypatch,[payload])
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,local_tool_policy=p) as proxy:
        client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=5)
        client.request('POST','/v1/messages',json.dumps({'model':m.MODEL,'max_tokens':100}))
        result=client.getresponse().read();client.close()
        assert b'"type": "error"' in result and b'content_block_stop' not in result
        assert proxy.budget.entries[0]['estimated_usd'] is None
        assert proxy.budget.committed>0 and proxy.budget.max_requests==1
        assert len(requests)==1 and not p.tool_calls


def test_real_cli_reads_writes_and_finishes_against_simulated_provider(tmp_path,monkeypatch):
    # Claude real, HTTPS del proveedor sustituido en el proxy por SSE local determinista.
    import shutil
    cli=shutil.which('claude')
    if not cli:pytest.skip('Claude CLI no instalado en este entorno')
    m=module();b=budget_module();case=tmp_path/'public';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('Lee inputs/data.csv; entrega reports/leakage/audit.md. Sin expected.')
    (case/'inputs/data.csv').write_text('x\n1\n');out=tmp_path/'run';root=out/'workspace'
    sequence=[sse(m.MODEL,[{'type':'tool_use','id':'read1','name':'Read','input':{'file_path':str(root/'inputs/data.csv')}}],'tool_use'),
              sse(m.MODEL,[{'type':'tool_use','id':'write1','name':'Write','input':{'file_path':str(root/'reports/leakage/audit.md'),'content':'## Resumen\nReporte del proveedor simulado; no evidencia de eficacia.\n'}}],'tool_use'),
              sse(m.MODEL,[{'type':'text','text':'Reporte guardado en reports/leakage/audit.md.'}],'end_turn')]
    requests=fake_upstream(b,monkeypatch,sequence)
    with b.Proxy('claude','fake-not-a-secret',.2,model=m.MODEL,max_requests=8,max_output_tokens=8192) as proxy:
        result=m.invoke(case,out,proxy,cli)
        assert result['runtime_success'],(result,(out/'stderr.txt').read_text(),(out/'stdout.jsonl').read_text())
        assert len(requests)==3 and result['request_count']==3
        assert [e['provider_stop_reason'] for e in proxy.budget.entries]==['tool_use','tool_use','end_turn']
        assert [x['name'] for x in result['tool_calls']]==['Read','Write']
        assert (root/'reports/leakage/audit.md').is_file()
        assert all(e['estimated_usd'] is not None for e in proxy.budget.entries)
        assert not result['skill_invoked']
        assert root/'.runtime/check_inputs.py' in proxy.local_tool_policy.hashes
        assert all('PRIVATE_EXPECTED' not in json.dumps(x) for x in requests)


def test_proxy_transport_failure_blocks_next_provider_request(tmp_path,monkeypatch):
    m,p=policy(tmp_path);b=budget_module();forwarded=[]
    class Connection:
        def __init__(self,*args,**kwargs):pass
        def request(self,*args,**kwargs):forwarded.append(1);raise OSError('simulated failure')
        def close(self):pass
    monkeypatch.setattr(b.http.client,'HTTPSConnection',Connection)
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,local_tool_policy=p) as proxy:
        for attempt in range(2):
            client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=5)
            client.request('POST','/v1/messages',json.dumps({'model':m.MODEL,'max_tokens':100}))
            try:client.getresponse().read()
            except b.http.client.RemoteDisconnected:pass
            client.close()
        assert len(forwarded)==1
        assert len(proxy.budget.entries)==1 and proxy.budget.entries[0]['estimated_usd'] is None


@pytest.mark.parametrize('attack',['external_read','input_write','arbitrary_bash'])
def test_real_cli_never_executes_forbidden_provider_tool(tmp_path,monkeypatch,attack):
    import shutil
    cli=shutil.which('claude')
    if not cli:pytest.skip('Claude CLI no instalado')
    m=module();b=budget_module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('Public case');(case/'inputs/data.csv').write_text('x\n1\n')
    private=tmp_path/'expected.md';private.write_text('PRIVATE_EXPECTED_MARKER')
    out=tmp_path/'run';root=out/'workspace';side_effect=tmp_path/'side-effect'
    if attack=='external_read':name,args='Read',{'file_path':str(private)}
    elif attack=='input_write':name,args='Write',{'file_path':str(root/'inputs/data.csv'),'content':'MUTATED'}
    else:name,args='Bash',{'command':'touch '+str(side_effect)}
    requests=fake_upstream(b,monkeypatch,[sse(m.MODEL,[{'type':'tool_use','id':'bad1','name':name,'input':args}],'tool_use')])
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,max_requests=8,max_output_tokens=8192) as proxy:
        result=m.invoke(case,out,proxy,cli)
        assert not result['runtime_success'] and len(requests)==1
        assert len(proxy.budget.entries)==1 and proxy.budget.entries[0].get('tool_guard_error')
        assert not side_effect.exists()
        assert (root/'inputs/data.csv').read_text()=='x\n1\n'
        assert all('PRIVATE_EXPECTED_MARKER' not in json.dumps(x) for x in requests)
        assert 'PRIVATE_EXPECTED_MARKER' not in (out/'stdout.jsonl').read_text()


def test_real_cli_invokes_exact_skill_and_readonly_utility(tmp_path,monkeypatch):
    import shlex,shutil,sys
    cli=shutil.which('claude')
    if not cli:pytest.skip('Claude CLI no instalado')
    m=module();b=budget_module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('Public audit');(case/'inputs/data.csv').write_text('x\n1\n')
    skill=Path(__file__).parents[1]/'evaluations/foundry/2026-10-10-detect-leakage-01/snapshots/experiments/skills/detect-leakage/SKILL.md'
    out=tmp_path/'run';root=out/'workspace'
    command=shlex.join([sys.executable,str(root/'.runtime/check_inputs.py')])
    sequence=[sse(m.MODEL,[{'type':'tool_use','id':'skill1','name':'Skill','input':{'skill':m.SKILL}}],'tool_use'),
              sse(m.MODEL,[{'type':'tool_use','id':'bash1','name':'Bash','input':{'command':command}}],'tool_use'),
              sse(m.MODEL,[{'type':'tool_use','id':'write1','name':'Write','input':{'file_path':str(root/'reports/leakage/audit.md'),'content':'Reporte simulado; no eficacia de skill.'}}],'tool_use'),
              sse(m.MODEL,[{'type':'text','text':'Reporte guardado.'}],'end_turn')]
    requests=fake_upstream(b,monkeypatch,sequence)
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,max_requests=8,max_output_tokens=8192) as proxy:
        result=m.invoke(case,out,proxy,cli,skill=skill)
        assert result['runtime_success'],(result,(out/'stdout.jsonl').read_text())
        assert result['skill_invoked'] and len(requests)==4
        assert [x['name'] for x in result['tool_calls']]==['Skill','Bash','Write']
        # Contenido Foundry cargado por Skill aparece después en el contexto real del CLI.
        assert 'Auditoría dedicada' in json.dumps(requests[1],ensure_ascii=False) or 'auditoría dedicada' in json.dumps(requests[1],ensure_ascii=False)
        assert 'sha256' in json.dumps(requests[2])
        assert (root/'.runtime/plugin/skills/detect-leakage/SKILL.md').read_bytes()==skill.read_bytes()
        assert root/'.runtime/plugin/.claude-plugin/plugin.json' in proxy.local_tool_policy.hashes


def test_proxy_deleted_input_blocks_before_provider(tmp_path,monkeypatch):
    m,p=policy(tmp_path);b=budget_module()
    requests=fake_upstream(b,monkeypatch,[])
    (p.root/'inputs/data.csv').unlink()
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,local_tool_policy=p) as proxy:
        client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=5)
        client.request('POST','/v1/messages',json.dumps({'model':m.MODEL,'max_tokens':100}))
        response=client.getresponse();response.read();client.close()
        assert response.status==403 and not requests and not proxy.budget.entries
        assert proxy.budget.max_requests==0


def test_real_cli_receives_explicit_common_tool_limits(tmp_path,monkeypatch):
    import shutil,shlex,sys
    cli=shutil.which('claude')
    if not cli:pytest.skip('Claude CLI no instalado')
    m=module();b=budget_module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('public');(case/'inputs/data.csv').write_text('x\n1\n')
    out=tmp_path/'run';root=out/'workspace';command=shlex.join([sys.executable,str(root/'.runtime/check_inputs.py')])
    sequence=[sse(m.MODEL,[{'type':'tool_use','id':'bash1','name':'Bash','input':{'command':command}}],'tool_use'),
              sse(m.MODEL,[{'type':'tool_use','id':'write1','name':'Write','input':{'file_path':str(root/'reports/leakage/audit.md'),'content':'Mock infrastructure report'}}],'tool_use'),
              sse(m.MODEL,[{'type':'text','text':'Listo.'}],'end_turn')]
    requests=fake_upstream(b,monkeypatch,sequence)
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,max_requests=8,max_output_tokens=8192) as proxy:
        result=m.invoke(case,out,proxy,cli,report_word_limit=500)
        assert result['runtime_success']
        context=json.dumps(requests[0],ensure_ascii=False)
        assert 'Contrato operativo de herramientas' in context
        assert 'máximo 500 palabras' in context
        assert 'Si está instalada, invócala al inicio mediante Skill' in context
        assert command in context
        assert 'sin prefijos, sufijos, argumentos adicionales ni comandos encadenados' in context
        assert str(root/'reports/leakage/audit.md') in context


def test_real_cli_preserves_invalid_report_and_prompt_then_closes_budget(tmp_path,monkeypatch):
    import hashlib,shutil
    cli=shutil.which('claude')
    if not cli:pytest.skip('Claude CLI no instalado')
    m=module();b=budget_module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('Auditar expediente');(case/'inputs/data.csv').write_text('x\n1\n')
    out=tmp_path/'run';root=out/'workspace';invalid='## Resumen\nFaltan los campos del contrato.\n'
    sequence=[sse(m.MODEL,[{'type':'tool_use','id':'write1','name':'Write','input':{'file_path':str(root/'reports/leakage/audit.md'),'content':invalid}}],'tool_use'),
              sse(m.MODEL,[{'type':'text','text':'Informe guardado.'}],'end_turn')]
    requests=fake_upstream(b,monkeypatch,sequence)
    with b.Proxy('claude','fake-not-a-secret',.2,model=m.MODEL,max_requests=8,max_output_tokens=8192) as proxy:
        result=m.invoke(case,out,proxy,cli,report_word_limit=500)
        assert result['runtime_success'] is True and result['contract_success'] is False
        assert result['execution_success'] is False and proxy.budget.max_requests==2
        assert (root/'reports/leakage/audit.md').read_text()==invalid
        prompt=(out/'prompt.txt').read_text()
        assert prompt in json.dumps(requests[0],ensure_ascii=False).replace('\\n','\n')
        assert hashlib.sha256((out/'prompt.txt').read_bytes()).hexdigest()==result['prompt_sha256']
        assert json.loads((out/'report-contract.json').read_text())['success'] is False


@pytest.mark.parametrize('with_skill',[False,True])
def test_real_cli_accepts_contract_without_claiming_semantic_quality(tmp_path,monkeypatch,with_skill):
    import hashlib,shutil
    cli=shutil.which('claude')
    if not cli:pytest.skip('Claude CLI no instalado')
    m=module();b=budget_module();case=tmp_path/'case';(case/'inputs').mkdir(parents=True)
    (case/'case.md').write_text('Auditar expediente');(case/'inputs/data.csv').write_text('x\n1\n')
    out=tmp_path/'run';root=out/'workspace'
    skill=Path(__file__).parents[1]/'evaluations/foundry/2026-10-11-detect-leakage-v02/draft/skills/detect-leakage/SKILL.md' if with_skill else None
    content='---\nskill: '+('detect-leakage' if with_skill else 'none')+'\nversion: '+('"0.2.0"' if with_skill else 'null')+'\nfecha: 2026-10-12\nestado: auditoria\ncondicion: '+('treatment' if with_skill else 'baseline')+'\ninputs:\n'
    for path in ['case.md','inputs/data.csv']:
        content+=f'  - path: {path}\n    sha256: {hashlib.sha256((case/path).read_bytes()).hexdigest()}\n'
    content+='---\n'
    for section in ['Resumen','Hallazgos','Evidencia','Preguntas abiertas','Recomendaciones']:
        content+=f'## {section}\nProveedor simulado; correctitud no evaluada.\n'
    sequence=[sse(m.MODEL,[{'type':'tool_use','id':'write1','name':'Write','input':{'file_path':str(root/'reports/leakage/audit.md'),'content':content}}],'tool_use'),
              sse(m.MODEL,[{'type':'text','text':'Reporte en reports/leakage/audit.md.'}],'end_turn')]
    if with_skill:sequence.insert(0,sse(m.MODEL,[{'type':'tool_use','id':'skill1','name':'Skill','input':{'skill':m.SKILL}}],'tool_use'))
    fake_upstream(b,monkeypatch,sequence)
    with b.Proxy('claude','fake-not-a-secret',.2,model=m.MODEL,max_requests=8,max_output_tokens=8192) as proxy:
        result=m.invoke(case,out,proxy,cli,report_word_limit=500,skill=skill)
        assert result['runtime_success'] and result['contract_success'] and result['execution_success']
        assert proxy.budget.max_requests==8
        contract=json.loads((out/'report-contract.json').read_text())
        assert contract['semantic_review']=='REQUIRED'
        assert (root/'reports/leakage/audit.md').read_text()==content
        assert result['skill_invoked'] is with_skill


def test_proxy_keeps_redacted_rejected_tool_input(tmp_path,monkeypatch):
    m,p=policy(tmp_path);b=budget_module();key='fake-private-api-key'
    attempted={'command':'cat ../expected.md; echo '+key+' sk-ant-private-test-secret-value','token':'private-token-value'}
    requests=fake_upstream(b,monkeypatch,[sse(m.MODEL,[{'type':'tool_use','id':'bad1','name':'Bash','input':attempted}],'tool_use')])
    with b.Proxy('claude',key,.2,model=m.MODEL,local_tool_policy=p) as proxy:
        client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=5)
        client.request('POST','/v1/messages',json.dumps({'model':m.MODEL,'max_tokens':100}))
        client.getresponse().read();client.close()
        entry=proxy.budget.entries[0]
        diagnostic=entry.get('rejected_tool')
        assert diagnostic is not None
        assert diagnostic['name']=='Bash' and '../expected.md' in diagnostic['input_preview']
        serialized=json.dumps(entry)
        assert key not in serialized and 'sk-ant-private-test-secret-value' not in serialized and 'private-token-value' not in serialized
        assert '[REDACTED]' in serialized and len(diagnostic['input_preview'])<=8192
        assert len(requests)==1 and not p.tool_calls


def test_rejection_diagnostic_is_bounded_and_redacts_sensitive_fields():
    b=budget_module();key='known-private-key'
    result=b.tool_diagnostic('Bash',{'command':'echo Bearer bearer-private-value '+key,'api_key':'other-private-key','nested':{'password':'private-password'},'large':'x'*20000},key)
    text=json.dumps(result)
    assert all(secret not in text for secret in [key,'bearer-private-value','other-private-key','private-password'])
    assert len(result['input_preview'])<=8192 and result['truncated']
    assert '[REDACTED]' in text


def test_proxy_stops_if_observed_input_exceeds_reserved_token_bound(tmp_path,monkeypatch):
    m,p=policy(tmp_path);b=budget_module()
    response=sse(m.MODEL,[{'type':'tool_use','id':'r1','name':'Read','input':{'file_path':str(p.root/'case.md')}}],'tool_use').replace(b'"input_tokens": 30',b'"input_tokens": 18000')
    fake_upstream(b,monkeypatch,[response])
    with b.Proxy('claude','fake-key',.2,model=m.MODEL,local_tool_policy=p) as proxy:
        client=b.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port,timeout=5)
        client.request('POST','/v1/messages',json.dumps({'model':m.MODEL,'max_tokens':100}))
        client.getresponse().read();client.close()
        entry=proxy.budget.entries[0]
        assert entry['usage']['input_tokens']>entry['input_token_bound']
        assert entry['estimated_usd']<entry['reserved_usd']
        assert entry['bound_exceeded'] and not p.tool_calls
        assert proxy.budget.max_requests==1
