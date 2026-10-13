from pathlib import Path
import json,hashlib,subprocess,sys,shutil
from datetime import datetime,timezone
root=Path.cwd();out=root/'evaluations/operational-selection/2026-10-08-selection-probe-02';py=root/'.venv/bin/python';runner=root/'scripts/evaluations/selection_runner.py'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def js(p,obj):p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def integrity():
 fr=json.loads((out/'preregister.json').read_text())['files'];assert all(digest(out/k)==v for k,v in fr.items())
 for live,frozen in [('scripts/evaluations/selection_runner.py','frozen/selection_runner.py'),('scripts/evaluations/selection_checker.py','frozen/selection_checker.py'),('schemas/selection-audit-0.1.0.schema.json','frozen/selection-audit-0.1.0.schema.json')]:assert digest(root/live)==digest(out/frozen)
integrity();version=subprocess.check_output([shutil.which('claude'),'--version'],text=True).strip()
js(out/'execution-record.json',{'started_at':datetime.now(timezone.utc).isoformat(),'cli_version':version,'driver_sha256':digest(Path(__file__)),'argv':[str(py),str(Path(__file__).resolve())]})
count=0
for rep in [1,2]:
 for case in 'ABCDEF':
  order=['baseline','treatment'] if (case in 'ACE')==(rep==1) else ['treatment','baseline']
  for condition in order:
   integrity();dest=out/'runs'/case/condition/str(rep)
   argv=[str(py),str(runner),'--payload-file',str(out/'payloads'/case/(condition+'.txt')),'--output-dir',str(dest)]
   result=subprocess.run(argv,capture_output=True,text=True)
   if not (dest/'metadata.json').exists():
    js(out/'execution-error.json',{'case':case,'condition':condition,'rep':rep,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr});sys.exit(2)
   js(dest/'runner-invocation.json',{'argv':argv,'exit_code':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
   meta=json.loads((dest/'metadata.json').read_text());count+=1;parsed={}
   if meta['schema_conformant']:
    cmd=[str(py),str(out/'frozen/selection_checker.py'),str(dest/'structured-output.json'),str(out/'cases'/case/'expected.json')]
    check=subprocess.run(cmd,capture_output=True,text=True);(dest/'content-check.json').write_text(check.stdout)
    js(dest/'content-check-request.json',{'argv':cmd,'exit_code':check.returncode,'stderr':check.stderr})
    if check.returncode:
     print('STOP: checker roto; preservar evidencia.',flush=True);sys.exit(5)
    parsed=json.loads(check.stdout)
   print(json.dumps({'call':count,'case':case,'condition':condition,'rep':rep,'runtime':meta['runtime_success'],'schema':meta['schema_conformant'],'model':meta['model_matches'],'mismatches':parsed.get('mismatches'),'cost':meta['cost_usd_reported']}),flush=True)
   if not meta['runtime_success'] or not meta['model_matches'] or meta['cli_version']!=version:
    print('STOP: infraestructura/configuración; intento conservado.',flush=True);sys.exit(4)
integrity();js(out/'execution-completed.json',{'finished_at':datetime.now(timezone.utc).isoformat(),'calls':count,'frozen_inputs_unchanged':True})
