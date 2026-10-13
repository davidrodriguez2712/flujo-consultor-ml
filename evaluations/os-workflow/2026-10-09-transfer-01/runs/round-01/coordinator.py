from pathlib import Path
from datetime import datetime,timezone
import hashlib,importlib.util,json,os,shlex,subprocess
R=Path('/Users/davidrodriguez/Programming/ai-flujo-consultor-ml');P=R/'evaluations/os-workflow/2026-10-09-transfer-01';C=P/'execution-config-01';OUT=P/'runs/round-01'
def now():return datetime.now(timezone.utc).isoformat()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
assert sha(C/'execution-manifest-01.json')=='69529a3f59f7eb3c214a5ebfaa64b8a0e50610f1a366efdd6493443b0b6601a4'
assert sha(P/'evidence-manifest-01.json')=='ee7a0d2a15b46a82cf6a986f694d9023e9f2c3fb48825ef1560365f7d6453650'
for home,name in [(P,'evidence-manifest-01.json'),(C,'execution-manifest-01.json')]:
 for row in json.loads((home/name).read_text())['files']:assert sha(home/row['path'])==row['sha256'],'Integridad de paquete/configuración'
for row in json.loads((C/'execution-manifest-01.json').read_text())['files']:
 if row['path'].startswith('snapshots/'):
  rel=Path(row['path']).relative_to('snapshots')
  assert sha(C/row['path'])==sha(R/rel),'Código activo diferente del snapshot listado'
cfg=json.loads((C/'config.json').read_text())
assert json.loads((P/'review-approval.json').read_text())['manifest_sha256']==sha(P/'evidence-manifest-01.json')
S=C/'snapshots'
T=load('transport',S/'scripts/evaluations/workflow_native_transport.py');B=load('budget',S/'scripts/ci/runtime_budget.py');K=load('checker',S/'scripts/evaluations/workflow_transfer_checker.py')
limit=T.require_approval(json.loads((P/'budget-approval.json').read_text()),sha(C/'execution-manifest-01.json'))
assert limit==cfg['budget']['proposed_total_usd']==0.10
assert cfg['isolation']['system_prompt']==T.TRANSFER_SYSTEM and cfg['runtime']['model']==T.MODEL
cli=cfg['runtime']['executable'];version=subprocess.run([cli,'--version'],capture_output=True,text=True,check=True).stdout.strip()
assert version==cfg['runtime']['version'],'Versión CLI distinta; detener antes de credencial/request'
helptext=subprocess.run([cli,'--help'],capture_output=True,text=True,check=True).stdout
flags=['--bare','--safe-mode','--no-chrome','--no-session-persistence','--disable-slash-commands','--tools','--strict-mcp-config','--mcp-config','--setting-sources','--effort','--model','--system-prompt','--output-format']
assert all(f in helptext for f in flags),'CLI incompatible'
put(P/'execution-preflight-01.json',{'status':'PASS_BEFORE_PROVIDER','at_utc':now(),'manifest_integrity':'PASS','snapshots_match':'PASS','approval_bound':'PASS','runtime_version':version,'flags_present':True,'max_new_budget_usd':limit,'actual_provider_compatibility':'PENDING_SMOKE','api_calls':0})
# Solo una variable desde .env, sin ejecutar shell ni copiar/hash/imprimir el secreto.
key=os.environ.get('ANTHROPIC_API_KEY')
if not key:
 values=[]
 for line in (R/'.env').read_text().splitlines():
  line=line.strip()
  if line.startswith('export '):line=line[7:].lstrip()
  name,sep,value=line.partition('=')
  if sep and name.strip()=='ANTHROPIC_API_KEY':
   parts=shlex.split(value,comments=True)
   if len(parts)!=1:raise ValueError('Variable Anthropic inválida')
   values.append(parts[0])
 if len(values)!=1 or not values[0]:raise ValueError('Falta variable Anthropic única')
 key=values[0]
OUT.mkdir(parents=True,exist_ok=False)
(OUT/'coordinator.py').write_text(Path(__file__).read_text())
state={'status':'RUNNING','started_at_utc':now(),'runtime_version':version,'model':T.MODEL,'approved_new_budget_usd':limit,'prior_study_estimated_usd':0.02065453,'completed_invocations':[],'benchmark_completed':0,'semantic_review':'NOT_RUN'}
def record(proxy):
 known=all(e['estimated_usd'] is not None for e in proxy.budget.entries)
 subtotal=sum(e['estimated_usd'] for e in proxy.budget.entries if e['estimated_usd'] is not None)
 state.update(provider_requests=len(proxy.budget.entries),usage_complete=known,known_cost_subtotal_usd=subtotal,estimated_new_api_cost_usd=subtotal if known else None,estimated_cumulative_studies_usd=0.02065453+subtotal if known else None,committed_budget_usd=proxy.budget.committed)
 put(OUT/'budget-ledger.json',{'new_limit_usd':limit,'entries':proxy.budget.entries,'rejections':proxy.rejections,'prior_study_estimated_usd':0.02065453,'execution_manifest_sha256':sha(C/'execution-manifest-01.json')})
 put(OUT/'round-status.json',state)
with B.Proxy('claude',key,limit,model=T.MODEL,max_requests=13,max_output_tokens=8192) as proxy:
 try:
  result=T.invoke((C/'smoke-payload.txt').read_text(),OUT/'smoke',proxy,cli,system_prompt=T.TRANSFER_SYSTEM)
  state['completed_invocations'].append('smoke');record(proxy)
  if not result['runtime_success'] or proxy.budget.entries[-1].get('provider_stop_reason')!='end_turn':raise ValueError('Smoke: fallo de runtime/stopreason')
  checked=K.check_text((OUT/'smoke/result.txt').read_text(),{'status':'READY','format':'markdown'},[]);put(OUT/'smoke/checks.json',checked)
  if not all(checked[k] is True for k in ('format_pass','status_matches','references_exist')):raise ValueError('Smoke: fallo de contrato')
  print(json.dumps({'invocation':'smoke','runtime':'PASS','format':'PASS','new_cost_usd':state['estimated_new_api_cost_usd']}),flush=True)
  for item in cfg['order']:
   cid=item['case'];identifier=cid+'-'+item['condition'];target=OUT/identifier
   result=T.invoke((P/item['payload']).read_text(),target,proxy,cli,system_prompt=T.TRANSFER_SYSTEM)
   state['completed_invocations'].append(identifier);record(proxy)
   if not result['runtime_success'] or proxy.budget.entries[-1].get('provider_stop_reason')!='end_turn':raise ValueError(identifier+': fallo runtime/stopreason; no retry')
   expected=json.loads((P/f'reviewer/expected/{cid}.json').read_text());artifacts=json.loads((P/f'agent_inputs/{cid}/artifacts.json').read_text())
   checked=K.check_text((target/'result.txt').read_text(),expected,list(artifacts));put(target/'deterministic-checks.json',checked)
   state['benchmark_completed']+=1;record(proxy)
   print(json.dumps({'invocation':identifier,'runtime':'PASS','format_pass':checked['format_pass'],'status_matches':checked['status_matches'],'new_cost_usd':state['estimated_new_api_cost_usd']}),flush=True)
  state['status']='RESPONSES_COLLECTED_PENDING_SEMANTIC_REVIEW'
 except Exception as exc:
  state.update(status='STOPPED',stop_reason=str(exc).replace(key,'[REDACTED]')[:300])
  print(json.dumps({'status':'STOPPED','reason':state['stop_reason']}),flush=True)
 finally:
  state['finished_at_utc']=now();record(proxy)
