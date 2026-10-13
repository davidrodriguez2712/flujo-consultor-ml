from pathlib import Path
import json,hashlib,subprocess,shutil,math
from datetime import datetime,timezone
root=Path.cwd();out=root/'evaluations/operational-selection/2026-10-08-selection-probe-02'
def js(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
assert json.loads((out/'execution-completed.json').read_text())['calls']==24
checks=[];summary={};names=['members_match','order_match','ranking_match','capacity_match','value_match','feasibility_match','optimality_match','causal_status_match','metrics_match','gate_matches']
for cond in ['baseline','treatment']:
 s={'calls':0,'runtime_success':0,'schema_conformant':0,'model_matches':0,'outputs_all_checked_fields_match':0,**{k:0 for k in names},'cost_usd_reported':0,'wall_seconds':0,'provider_duration_ms':0}
 for case in 'ABCDEF':
  for rep in [1,2]:
   d=out/'runs'/case/cond/str(rep);m=json.loads((d/'metadata.json').read_text());s['calls']+=1
   for k in ['runtime_success','schema_conformant','model_matches']:s[k]+=int(m[k])
   s['cost_usd_reported']+=m['cost_usd_reported'];s['wall_seconds']+=m['wall_seconds'];s['provider_duration_ms']+=m['provider_duration_ms']
   argv=[str(root/'.venv/bin/python'),str(out/'frozen/selection_checker.py'),str(d/'structured-output.json'),str(out/'cases'/case/'expected.json')]
   fresh=json.loads(subprocess.check_output(argv,text=True));assert fresh==json.loads((d/'content-check.json').read_text())
   for k in names:s[k]+=int(fresh[k])
   s['outputs_all_checked_fields_match']+=int(not fresh['mismatches'])
   checks.append({'case':case,'condition':cond,'repetition':rep,'result':fresh})
 for k in ['cost_usd_reported','wall_seconds']:s[k]=round(s[k],7)
 summary[cond]=s
js(out/'deterministic-checks.json',checks);js(out/'summary.json',summary)
# Wald declarado en outputs E: verificar solo los cálculos numéricos, no acreditar supuestos de muestreo.
ci=[]
for stratum,p0,p1,clv,cost in [('G1',.6,.7,100,5),('G2',.7,.74,200,2),('G3',.8,.79,300,1)]:
 delta=p1-p0;se=math.sqrt((p0*(1-p0)+p1*(1-p1))/10000);net=delta*clv-cost
 ci.append({'stratum':stratum,'effect':delta,'effect_ci95':[delta-1.96*se,delta+1.96*se],'net_value':net,'net_ci95':[net-1.96*se*clv,net+1.96*se*clv]})
se_sum=math.sqrt((.6*.4+.7*.3)/10000*100**2+(.7*.3+.74*.26)/10000*200**2)
js(out/'additional-ci-arithmetic.json',{'method':'Aproximación Wald/no pooled y estratos independientes, como declaran outputs E; comprobación aritmética, sin validar supuestos reales ni cobertura postselección.','strata':ci,'selected_value_ci95':[11-1.96*se_sum,11+1.96*se_sum]})
fr=json.loads((out/'preregister.json').read_text());assert all(hashlib.sha256((out/p).read_bytes()).hexdigest()==h for p,h in fr['files'].items())
previous=[]
for rel in ['delayed-outcomes/2026-10-07-contract-probe','operational-selection/2026-10-07-playbook-probe','evidence-to-recommendation/2026-10-07-template-probe','delayed-outcomes/2026-10-07-contract-probe-02','engineering/2026-10-07-structured-runner-v02-check','delayed-outcomes/2026-10-08-contract-probe-03']:
 d=root/'evaluations'/rel;f=json.loads((d/'evidence-manifest.json').read_text())['files'];assert all(hashlib.sha256((d/p).read_bytes()).hexdigest()==h for p,h in f.items());previous.append(len(f))
pilot=root/'pilots/churn-retencion-sintetico';n=0
for name in ['handoff/handoff-manifest-02-closed.json','delivery/delivery-manifest.json']:
 for f in json.loads((pilot/name).read_text())['files']:
  b=(pilot/f['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes'];n+=1
first=min(json.loads(p.read_text())['started_at'] for p in (out/'runs').glob('*/*/*/metadata.json'));assert fr['frozen_at']<first
js(out/'integrity-check.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'frozen_files':len(fr['files']),'first_call_started_at':first,'local_freeze_before_first_call':True,'previous_file_counts':previous,'previous_total':sum(previous),'pilot_protected_entries':n,'all_unchanged':True,'checks_reproduced':len(checks)})
shutil.copyfile(__file__,out/'aggregation-driver.py');print(json.dumps(summary,indent=2))
