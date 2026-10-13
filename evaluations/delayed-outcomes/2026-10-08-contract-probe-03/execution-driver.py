from pathlib import Path
import json,hashlib,subprocess,sys,shutil
from datetime import datetime,timezone
root=Path.cwd();out=root/'evaluations/delayed-outcomes/2026-10-08-contract-probe-03';py=root/'.venv/bin/python'; runner=root/'scripts/evaluations/temporal_runner.py'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def integrity():
 frozen=json.loads((out/'preregister.json').read_text())['files'];bad=[k for k,v in frozen.items() if digest(out/k)!=v]
 assert not bad,bad
 assert digest(runner)==digest(out/'frozen/temporal_runner.py')
 assert digest(root/'schemas/temporal-audit-0.1.0.schema.json')==digest(out/'frozen/temporal-audit-0.1.0.schema.json')
integrity()
cli=shutil.which('claude');version=subprocess.check_output([cli,'--version'],text=True).strip()
shutil.copyfile(__file__,out/'execution-driver.py')
js(out/'execution-record.json',{'started_at':datetime.now(timezone.utc).isoformat(),'cli_version':version,'driver_sha256':digest(out/'execution-driver.py'),'argv':[str(py),__file__],'review':'Auto revisión del autor antes de freeze; sin reviewer externo.'})
count=0
for rep in [1,2]:
 for case in 'ABCDEF':
  order=['baseline','treatment'] if (case in 'ACE')==(rep==1) else ['treatment','baseline']
  for condition in order:
   integrity()
   dest=out/'runs'/case/condition/str(rep)
   argv=[str(py),str(runner),'--payload-file',str(out/'payloads'/case/(condition+'.txt')),'--output-dir',str(dest)]
   result=subprocess.run(argv,capture_output=True,text=True)
   if not dest.exists():
    print(json.dumps({'case':case,'condition':condition,'rep':rep,'error':result.stdout,'stderr':result.stderr}),flush=True);sys.exit(2)
   js(dest/'runner-invocation.json',{'argv':argv,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
   meta=json.loads((dest/'metadata.json').read_text());count+=1
   if (dest/'structured-output.json').exists():
    cmd=[str(py),str(out/'checker/check.py'),str(dest/'structured-output.json'),str(out/'cases'/case/'expected.json')]
    check=subprocess.run(cmd,capture_output=True,text=True);(dest/'content-check.json').write_text(check.stdout)
    js(dest/'content-check-request.json',{'argv':cmd,'exit_code':check.returncode,'stderr':check.stderr})
    parsed=json.loads(check.stdout) if check.returncode==0 else {}
   else:parsed={}
   print(json.dumps({'call':count,'case':case,'condition':condition,'rep':rep,'runtime':meta['runtime_success'],'schema':meta['schema_conformant'],'model':meta['model_matches'],'fields':parsed.get('field_matches'),'decisions':parsed.get('row_decisions_correct'),'cost':meta['cost_usd_reported']}),flush=True)
   if result.returncode or meta['cli_version']!=version:
    print('STOP: infraestructura/configuración; intento conservado.',flush=True);sys.exit(4)
integrity();js(out/'execution-completed.json',{'finished_at':datetime.now(timezone.utc).isoformat(),'calls':count,'frozen_inputs_unchanged':True})
