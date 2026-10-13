from pathlib import Path
import json,hashlib,subprocess,sys
from datetime import datetime,timezone
root=Path.cwd();out=root/'evaluations/delayed-outcomes/2026-10-08-contract-probe-03'
def js(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Categorías interpretativas asignadas por el autor después de leer razones/preguntas completas.
category={
('A','baseline',1):'ROORO',('A','baseline',2):'RRRPO',('A','treatment',1):'ROR',('A','treatment',2):'RRRO',
('B','baseline',1):'NNNOR',('B','baseline',2):'NNNRO',('B','treatment',1):'NNNRON',('B','treatment',2):'NNNOOO',
('C','baseline',1):'PRRO',('C','baseline',2):'ROROR',('C','treatment',1):'OROO',('C','treatment',2):'ORRO',
('D','baseline',1):'OORO',('D','baseline',2):'ROORR',('D','treatment',1):'ORO',('D','treatment',2):'ROOR',
('E','baseline',1):'NNOR',('E','baseline',2):'NOOR',('E','treatment',1):'NORO',('E','treatment',2):'NORO',
('F','baseline',1):'NNNO',('F','baseline',2):'NNO',('F','treatment',1):'NNOR',('F','treatment',2):'NNNR'}
labels={'N':'necesaria','R':'redundante','O':'opcional_contextual','P':'problematica'}
manual=[];checks=[];summaries={}
for cond in ['baseline','treatment']:
 s={'calls':0,'runtime_success':0,'schema_conformant':0,'model_matches':0,'gate_matches':0,'ids_exact':0,'field_matches':0,'field_total':0,'row_decisions_correct':0,'row_total':0,'eligible_false_positives':0,'valid_rows_excluded':0,'valid_rows_indeterminate':0,'reason_errors':0,'questions':{label:0 for label in labels.values()},'outputs_with_redundant_questions':0,'outputs_with_problematic_questions':0,'cost_usd_reported':0,'wall_seconds':0,'provider_duration_ms':0}
 for case in 'ABCDEF':
  for rep in [1,2]:
   d=out/'runs'/case/cond/str(rep);m=json.loads((d/'metadata.json').read_text());o=json.loads((d/'structured-output.json').read_text())
   # Reproducir checker congelado; no modificar expected ni output.
   cmd=[str(root/'.venv/bin/python'),str(out/'checker/check.py'),str(d/'structured-output.json'),str(out/'cases'/case/'expected.json')]
   fresh=json.loads(subprocess.check_output(cmd,text=True));prior=json.loads((d/'content-check.json').read_text());assert fresh==prior
   c=category[case,cond,rep];assert len(c)==len(o['open_questions']),(case,cond,rep)
   s['calls']+=1
   for k in ['runtime_success','schema_conformant','model_matches']:s[k]+=int(m[k])
   for k in ['gate_matches','ids_exact','field_matches','field_total','row_decisions_correct','row_total','eligible_false_positives','valid_rows_excluded','valid_rows_indeterminate']:s[k]+=int(fresh[k])
   s['cost_usd_reported']+=m['cost_usd_reported'];s['wall_seconds']+=m['wall_seconds'];s['provider_duration_ms']+=m['provider_duration_ms']
   for k in c:s['questions'][labels[k]]+=1
   s['outputs_with_redundant_questions']+=int('R' in c);s['outputs_with_problematic_questions']+=int('P' in c)
   entries=[{'index':i+1,'category':labels[k],'text':q} for i,(k,q) in enumerate(zip(c,o['open_questions']))]
   notes=[]
   if (case,cond,rep)==('A','baseline',2):
    notes.append({'question_index':4,'issue':'La retirada se equipara a churn=0 sin una regla de certificación de negativos. El caso solo proporciona certificación positiva por vencimiento sin retirada; no autoriza inferir negativo definitivo al retirar.'})
   if (case,cond,rep)==('C','baseline',1):
    notes.append({'question_index':1,'issue':'Propone cambiar pending si el acta se publicó antes de extracción, aunque la regla exige cerrar la ventana el 1 de septiembre, posterior a extracción. La hipótesis contradice la regla de certificación conocida.'})
   manual.append({'case':case,'condition':cond,'repetition':rep,'reviewer':'autor; no ciego ni independiente','rows':[{'id':r['id'],'reason_error':False,'note':'Razón coherente con reglas, evidencia y clasificación; sin contradicción material observada.'} for r in o['rows']],'question_entries':entries,'findings':notes})
   checks.append({'case':case,'condition':cond,'repetition':rep,'result':fresh})
 for k in ['cost_usd_reported','wall_seconds']:s[k]=round(s[k],7)
 summaries[cond]=s
js(out/'deterministic-checks.json',checks);js(out/'semantic-review.json',manual);js(out/'summary.json',summaries)
write='''# Revisión semántica — ronda 03
Revisión manual del autor, después de leer las 24 respuestas completas; no ciega, independiente ni humana externa. El checker no verifica razones ni pertinencia de preguntas. Ver semantic-review.json para el texto y clasificación de cada entrada y los 72 motivos revisados.

Las 72 razones (36 por condición) son coherentes con las decisiones y el caso: no se observó error material. Ambos distinguen solicitudes reversibles, publicación tardía, seguimiento incompleto, features reconstruidas y conflictos de igual autoridad. F1 permanece indeterminado, F2 respeta prioridad documentada y F3 conserva exclusión demostrada aun con conflicto de features.

Dos outputs baseline contienen preguntas problemáticas, una en cada repetición y en casos distintos. A/baseline/2, pregunta 4, equipara retirada a churn=0 sin certificación negativa documentada. C/baseline/1, pregunta 1, sugiere cambiar pending mediante un acta anterior a extracción aunque la regla exige cerrar la ventana el 1 de septiembre. No cambian sus decisiones finales correctas. No se observaron preguntas con contradicción equivalente en treatment.

Ambas condiciones generan preguntas redundantes y recomendaciones contextuales. Algunos elementos de open_questions son declaraciones, no preguntas: el schema admite strings y no verifica su forma interrogativa. Se clasifican como opcionales contextuales o redundantes según su contenido. Pedir evidencia independiente o proponer otra reconstrucción puede ser útil fuera del encargo y se cuenta como opcional; reconfirmar hechos explícitos para decidir el caso se cuenta como redundante. Estos recuentos requieren juicio y pueden cambiar con otro revisor.

La reducción de dos preguntas problemáticas a cero es una señal secundaria, no una ventaja demostrada en las decisiones temporales ni prueba suficiente para crear/promover una skill. No cumple la mejora decisional prospectiva en al menos dos escenarios. Las preguntas siguen siendo abundantes; merece considerar un criterio general de pertinencia antes de añadir más instrucciones a la validación temporal.
'''
(out/'review.md').write_text(write,encoding='utf-8')
# Revalidar freeze e integridad de evidencia previa.
fr=json.loads((out/'preregister.json').read_text());assert all(hashlib.sha256((out/p).read_bytes()).hexdigest()==h for p,h in fr['files'].items())
previous=[]
for rel in ['delayed-outcomes/2026-10-07-contract-probe','operational-selection/2026-10-07-playbook-probe','evidence-to-recommendation/2026-10-07-template-probe','delayed-outcomes/2026-10-07-contract-probe-02','engineering/2026-10-07-structured-runner-v02-check']:
 d=root/'evaluations'/rel;f=json.loads((d/'evidence-manifest.json').read_text())['files'];assert all(hashlib.sha256((d/p).read_bytes()).hexdigest()==h for p,h in f.items());previous.append(len(f))
pilot=root/'pilots/churn-retencion-sintetico';count=0
for name in ['handoff/handoff-manifest-02-closed.json','delivery/delivery-manifest.json']:
 for f in json.loads((pilot/name).read_text())['files']:
  b=(pilot/f['path']).read_bytes();assert hashlib.sha256(b).hexdigest()==f['sha256'] and len(b)==f['bytes'];count+=1
start=min(json.loads(p.read_text())['started_at'] for p in (out/'runs').glob('*/*/*/metadata.json'));assert fr['frozen_at']<start
js(out/'integrity-check.json',{'checked_at':datetime.now(timezone.utc).isoformat(),'frozen_files':len(fr['files']),'first_call_started_at':start,'local_freeze_before_first_call':True,'previous_file_counts':previous,'previous_total':sum(previous),'pilot_protected_entries':count,'all_unchanged':True,'checks_reproduced':len(checks)})
print(json.dumps(summaries,ensure_ascii=False,indent=2))
