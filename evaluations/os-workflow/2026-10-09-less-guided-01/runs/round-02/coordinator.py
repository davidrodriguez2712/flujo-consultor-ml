from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,os,shlex,subprocess
ROOT=Path('/Users/davidrodriguez/Programming/ai-flujo-consultor-ml')
BASE=ROOT/'evaluations/os-workflow/2026-10-09-less-guided-01'
CFG=BASE/'execution-config-02'
OUT=BASE/'runs/round-02'
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
for home,filename,expected in [(CFG,'execution-manifest-02.json','c844052205a518f94c5c4bbd02520749385f752be73abee59ef97a66791c2a41'),(BASE,'evidence-manifest-01.json','90544d163b168930e86373699ede98b7f099b54d1b7d7d5ea9487d1c50362e19')]:
    manifest=home/filename
    assert sha(manifest)==expected,'Manifest cambiado'
    assert all(sha(home/e['path'])==e['sha256'] for e in json.loads(manifest.read_text())['files']),'Archivo cambiado'
for snapshot in (CFG/'snapshots').rglob('*'):
    if snapshot.is_file():assert sha(snapshot)==sha(ROOT/snapshot.relative_to(CFG/'snapshots')),'Código diferente de snapshot'
transport=load_module('workflow_native_transport',ROOT/'scripts/evaluations/workflow_native_transport.py')
budget=load_module('runtime_budget',ROOT/'scripts/ci/runtime_budget.py')
checker=load_module('workflow_output_checker',ROOT/'scripts/evaluations/workflow_output_checker.py')
limit=transport.require_approval(json.loads((BASE/'budget-approval-02.json').read_text()),sha(CFG/'execution-manifest-02.json'))
config=json.loads((CFG/'config.json').read_text());cli=config['runtime']['executable']
prior_cost=config['budget']['prior_round_estimated_usd'];approved_total=limit;limit-=prior_cost
assert limit>0
assert sha(BASE/config['prior_round'])==config['prior_round_manifest_sha256']
version=subprocess.run([cli,'--version'],capture_output=True,text=True,check=True).stdout.strip()
assert version=='2.1.296 (Claude Code)','Versión distinta de revisión local'
helptext=subprocess.run([cli,'--help'],capture_output=True,text=True,check=True).stdout
flags=['--bare','--safe-mode','--no-chrome','--no-session-persistence','--disable-slash-commands','--tools','--strict-mcp-config','--mcp-config','--setting-sources','--effort','--model','--system-prompt','--output-format']
assert all(f in helptext for f in flags),'CLI incompatible'
# No shell sourcing ni carga de otras variables. No registrar contenido ni hash del secret.
key=os.environ.get('ANTHROPIC_API_KEY')
if not key:
    matches=[]
    for line in (ROOT/'.env').read_text().splitlines():
        text=line.strip()
        if text.startswith('export '):text=text[7:].lstrip()
        name,sep,value=text.partition('=')
        if sep and name.strip()=='ANTHROPIC_API_KEY':
            parts=shlex.split(value,comments=True)
            if len(parts)!=1:raise ValueError('Variable Anthropic inválida en .env')
            matches.append(parts[0])
    if len(matches)!=1 or not matches[0]:raise ValueError('No hay una clave Anthropic única en .env')
    key=matches[0]
OUT.mkdir(parents=True,exist_ok=False)
(OUT/'coordinator.py').write_text(Path(__file__).read_text(),encoding='utf-8')
write(OUT/'runtime-amendment.json',{'original_execution_manifest_sha256':sha(CFG/'execution-manifest-02.json'),'original_version':config['runtime']['version'],'reviewed_version':version,'required_flags_present':True,'reviewer':'Agente autor, revisión local','ruling':'Aceptar actualización patch para smoke de compatibilidad; conserva modelo, payloads, controles y presupuesto autorizados. No altera freeze previo.','recorded_at_utc':now(),'budget_authorization':'../../budget-approval.json','effective_runtime_compatibility':'PENDING_SMOKE'})
state={'status':'RUNNING','started_at_utc':now(),'runtime_version':version,'model':transport.MODEL,'approved_total_usd':approved_total,'prior_cost_usd':prior_cost,'completed_invocations':[],'benchmark_invocations_completed':0,'stop_reason':None,'semantic_review':'NOT_RUN'}
def record(proxy):
    state['provider_requests']=len(proxy.budget.entries)
    state['estimated_api_cost_usd']=sum(e['estimated_usd'] or 0 for e in proxy.budget.entries)
    state['cumulative_estimated_api_cost_usd']=prior_cost+state['estimated_api_cost_usd']
    state['cost_usage_complete']=all(e['estimated_usd'] is not None for e in proxy.budget.entries)
    state['committed_budget_usd']=proxy.budget.committed
    write(OUT/'budget-ledger.json',{'limit_usd':limit,'entries':proxy.budget.entries,'rejections':proxy.rejections,'prior_round_estimated_usd':prior_cost,'approved_cumulative_limit_usd':approved_total,'prior_round_manifest_sha256':config['prior_round_manifest_sha256']})
    write(OUT/'round-status.json',state)
with budget.Proxy('claude',key,limit,model=transport.MODEL,max_requests=13,max_output_tokens=8192) as proxy:
    try:
        result=transport.invoke((CFG/'smoke-payload.txt').read_text(),OUT/'smoke',proxy,cli)
        state['completed_invocations'].append('smoke');record(proxy)
        if not result['runtime_success']:raise ValueError('Smoke: fallo de runtime')
        if proxy.budget.entries[-1].get('provider_stop_reason')!='end_turn':raise ValueError('Smoke: stop reason upstream inesperado')
        checked=checker.check_text((OUT/'smoke/result.txt').read_text(),{'status':'READY'},[])
        write(OUT/'smoke/checks.json',checked)
        if not all(checked[k] is True for k in ('strict_json_pass','schema_pass','status_matches','references_exist')):raise ValueError('Smoke: fallo de contrato')
        print(json.dumps({'invocation':'smoke','runtime':'PASS','contract':'PASS','estimated_api_cost_usd':state['estimated_api_cost_usd']}),flush=True)
        for item in config['order']:
            identifier=item['case']+'-'+item['condition'];target=OUT/identifier
            result=transport.invoke((BASE/item['payload']).read_text(),target,proxy,cli)
            state['completed_invocations'].append(identifier)
            if not result['runtime_success'] or proxy.budget.entries[-1].get('provider_stop_reason')!='end_turn':
                record(proxy);raise ValueError(identifier+': fallo de runtime; conservar y no reintentar')
            # Revisor local separado: expected nunca se pasa a invoke.
            expected=json.loads((BASE/'reviewer/expected'/f"{item['case']}.json").read_text())
            artifacts=json.loads((BASE/'agent_inputs'/item['case']/'artifacts.json').read_text())
            checked=checker.check_text((target/'result.txt').read_text(),expected,list(artifacts))
            write(target/'deterministic-checks.json',checked)
            state['benchmark_invocations_completed']+=1;record(proxy)
            print(json.dumps({'invocation':identifier,'runtime':'PASS','format':checked['schema_pass'],'status_matches':checked['status_matches'],'estimated_api_cost_usd':state['estimated_api_cost_usd']}),flush=True)
        state['status']='RESPONSES_COLLECTED_PENDING_SEMANTIC_REVIEW'
    except Exception as exc:
        state['status']='STOPPED';state['stop_reason']=str(exc).replace(key,'[REDACTED]')[:300]
        print(json.dumps({'status':'STOPPED','reason':state['stop_reason']}),flush=True)
    finally:
        state['finished_at_utc']=now();record(proxy)
