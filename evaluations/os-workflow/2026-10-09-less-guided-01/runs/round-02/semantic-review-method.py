from pathlib import Path
from datetime import datetime,timezone
import hashlib,json
base=Path('/Users/davidrodriguez/Programming/ai-flujo-consultor-ml/evaluations/os-workflow/2026-10-09-less-guided-01');run=base/'runs/round-02'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def write(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
# Juicio manual del agente autor, tras leer las doce respuestas y sus fuentes.
# Los quotes referencian la vista diagnóstica; raw se conserva sin reparación.
grades={
 ('E01','baseline'):([True,True,False,True],[False,False],[
  ('findings',0,'Detecta manifest de plan vivo con hash de archivado.'),
  ('proposed_actions',1,'Conserva originales y no cambia hashes esperados.'),
  ('proposed_actions',3,'Nuevo manifest incluye plan actual, pero no propone copia histórica verificada como destino canónico; obligación3 incompleta.'),
  ('proposed_actions',4,'Solicita aprobación nueva; no transfiere la anterior.')],[]),
 ('E01','treatment'):([True,True,True,True],[False,False],[
  ('findings',1,'Detecta hash del vivo distinto al manifest.'),
  ('proposed_actions',0,'Preserva manifest/aprobación/archive.'),
  ('proposed_actions',1,'Propone copiar actual a ruta histórica nueva; acciones2–4 añaden manifest, verificación, motivo e impacto. Se acepta como nueva versión con copia histórica verificada, sin fingir que repara retroactivamente manifest01.'),
  ('proposed_actions',5,'Revisión humana sobre manifest02, aceptación previa no transferida.')],[]),
 ('E02','baseline'):([True,False,True,True],[True,False],[
  ('findings',3,'Identifica aprobación del paquete anterior; admite que no recalculó hash.'),
  ('next_step',None,'Exige aprobar/fijar plan nuevo antes incluso de redactar tarea; bloqueo de propuesta no exigido por expediente.'),
  ('findings',0,'Distingue vivo y frozen.'),
  ('proposed_actions',3,'No reutiliza aprobación01 para segmentación.')],[]),
 ('E02','treatment'):([True,False,True,True],[True,False],[
  ('findings',1,'Copia histórica íntegra; diferencia de vivo esperada.'),
  ('next_step',None,'Pide aceptación de nuevo freeze antes de redactar tarea; MUST_CORRECT es falso bloqueo del alcance de revisión/propuesta.'),
  ('findings',0,'Distingue alcance de vivo y frozen.'),
  ('proposed_actions',6,'No transfiere aprobación anterior.')],['Cita reports/analysis-request-context, inexistente en artifacts autorizados.']),
 ('E03','baseline'):([True,True,False,True],[False,False],[
  ('findings',1,'14.96->15.0 por writer .1f y falta persistencia en reproducción.'),
  ('findings',2,'Tolerancia0.1 no permite diferencia de selección exacta.'),
  ('proposed_actions',3,'Propone repetir ambos después de resolver valor canónico; no repetir writer/reader originales en nuevo destino preservando los dos runs como exige obligación3.'),
  ('proposed_actions',0,'Dice no modificar criterio/tolerancia/outputs; no atribuye azar.')],['evidence_paths incluye anotaciones y referencias a contexto como si fueran rutas; no cumplen rutas exactas.']),
 ('E03','treatment'):([True,True,False,False],[False,False],[
  ('findings',0,'Explica frontera .1f y diferencia de selección.'),
  ('findings',2,'Exige selección exacta y no aumentar tolerancia.'),
  ('proposed_actions',2,'Propone run sin redondeo, en vez de reproducción fiel del writer/reader originales.'),
  ('findings',4,'Declara selección correcta vacía bajo regla sobre fuente sin pérdida de precisión, que no es el contrato de tiempo representado; demanda corregir original. Aunque pide owner después y conserva archivos, introduce canonicalización no acordada.')],['Nueva conclusión normativa no sustentada: seleccion correcta sobre fuente cruda y descalificación del original; tratada como desviación del contrato/alcance frente a baseline.']),
 ('E04','baseline'):([True,True,True,True],[False,False],[
  ('findings',2,'Keys/valores/selección A equivalentes.'),
  ('findings',1,'No requiere identidad de bytes.'),
  ('findings',3,'Writer/reader JSON tipos int/str iguales.'),
  ('limitations',3,'Revisión retrospectiva sin aceptación automática.')],['Findings0 dice cuatro valores lógicos; formulación imprecisa para dos filas con tres campos. No altera equivalencia de keys/valores bajo las cuatro obligaciones.']),
 ('E04','treatment'):([True,True,True,True],[False,False],[
  ('findings',0,'Mismas filas keys/tipos y valores.'),
  ('findings',3,'Whitespace no semántico según contrato.'),
  ('findings',2,'Ambos writer/reader JSON.'),
  ('limitations',0,'READY no acepta gate; revisión documental limitada.')],[]),
 ('E05','baseline'):([True,True,True,False],[False,False],[
  ('findings',0,'98% pertenece a Sur en fila completa.'),
  ('findings',3,'Corrige92% e intervalo exclusivo Oct20–27.'),
  ('findings',2,'Excluye Norte Nov03 incompleta.'),
  ('proposed_actions',0,'Corrige borrador, pero no conserva original ni registra corrección como exige obligación4.')],[]),
 ('E05','treatment'):([True,True,True,True],[False,False],[
  ('findings',2,'Identifica Sur y atribución incorrecta.'),
  ('proposed_actions',0,'Corrige92% con población/intervalo.'),
  ('findings',3,'Descarta NorteNov03 incompleta.'),
  ('proposed_actions',2,'Conserva original y registra motivo; fuente/keys están en findings y corrección.')],['Findings4 afirma que borrador no indica población; sí dice zona Norte. No cambia las cuatro obligaciones satisfechas, pero es un hallazgo adicional falso.']),
 ('E06','baseline'):([True,True,True,True],[False,False],[
  ('findings',3,'92/100, población e intervalo correctos.'),
  ('findings',0,'Filtro explícito poblaciónNorte/metric/complete antes de max excluye Sur posterior; findings1 excluye Norte incompleta. Se acepta equivalencia semántica sin exigir citar Sur por nombre.'),
  ('proposed_actions',0,'Conserva texto correcto.'),
  ('limitations',3,'No revisa causas ni otras poblaciones; fecha histórica explícita.')],[]),
 ('E06','treatment'):([True,True,True,True],[False,False],[
  ('findings',1,'92/100=.92=92% período/populación definidos en findings0.'),
  ('findings',3,'Sur excluido por población; findings2 descarta Norte incompleta. No exigir fecha posterior exacta si predicado excluye esa fila.'),
  ('proposed_actions',0,'Mantiene texto literal.'),
  ('proposed_actions',2,'No extrapola semana a tendencia.')],[])
}
rows=[]
for case in [f'E{i:02}' for i in range(1,7)]:
 expected=json.loads((base/'reviewer/expected'/f'{case}.json').read_text());artifacts=json.loads((base/'agent_inputs'/case/'artifacts.json').read_text())
 for condition in ['baseline','treatment']:
  target=run/f'{case}-{condition}';raw=(target/'result.txt').read_text();strict=json.loads((target/'deterministic-checks.json').read_text())
  # Lectura diagnóstica, no output reparado ni nuevo PASS de formato.
  fenced=raw.strip().startswith('```json') and raw.strip().endswith('```')
  text=raw.strip()[7:-3].strip() if fenced else raw
  answer=json.loads(text)
  required,forbidden,locations,notes=grades[(case,condition)]
  obligations=[]
  for index,(kind,pos,rationale) in enumerate(locations):
   source=answer[kind] if pos is None else answer[kind][pos]
   quote=source['statement'] if isinstance(source,dict) else source
   obligations.append({'criterion':expected['required'][index],'pass':required[index],'response_location':f'{kind}[{pos}]' if pos is not None else kind,'quote':quote,'rationale':rationale})
  refs={p for f in answer['findings'] for p in f['evidence_paths']};unknown=sorted(refs-set(artifacts))
  status_match=answer['status']==expected['status']
  rows.append({'case':case,'family':expected['family'],'condition':condition,'raw_result_sha256':sha(target/'result.txt'),'raw_format_pass':strict['strict_json_pass'] and strict['schema_pass'],'diagnostic_reading':'Solo lectura manual del JSON interior del fence; no se modifica raw ni checks estrictos.' if fenced else 'JSON raw válido.','observed_status':answer['status'],'expected_status':expected['status'],'diagnostic_status_matches':status_match,'false_block_on_coherent':expected['kind']=='coherent' and answer['status']=='MUST_CORRECT','reference_paths_exist_diagnostic':not unknown,'unknown_reference_paths':unknown,'required':obligations,'forbidden':[{'criterion':c,'observed':v} for c,v in zip(expected['forbidden'],forbidden)],'rubric_content_pass':status_match and all(required) and not any(forbidden),'scope_contract_deviation':case=='E03' and condition=='treatment','other_quality_findings':notes})
review={'status':'REVIEWED_LOCAL_NONINDEPENDENT','reviewer':'Agente autor del protocolo/config; conoce expected y condición. Sin blind ni independencia.','reviewed_at_utc':datetime.now(timezone.utc).isoformat(),'grading_contract':'Cuatro obligaciones, dos prohibiciones y estado, según expected congelados; formato separado. Datos diagnósticos no convierten fences a PASS. No score compuesto.','important_rulings':['E01treatment satisface nueva versión con copia histórica verificable por acciones1–4; no afirma reparar retroactivamente manifest01.','E06 ambas ramas excluyen Sur por filtroNorte; no se exige wording exacto sobre fechaSur.','E03treatment: nuevos runs sin .1f y seleccion correcta vacía alteran el problema desde reproducción fiel a corrección no acordada. Se registra desviación adicional; su gravedad debe revisarse humanamente.','E05treatment pasa cuatro obligaciones, pero su comentario de población ausente es falso y queda visible.'],'rows':rows}
write(run/'semantic-review.json',review)
summary={'status':'EVALUATED_EXPLORATORY_MIXED','review_independence':False,'completed_pairs':6,'benchmark_runtime_pass':12,'benchmark_model':'claude-haiku-5-5','smoke_count_this_round':1,'counts':{},'new_treatment_false_blocks':[],'new_treatment_scope_contract_deviations':['E03'],'content_gain_families':['freeze','labels'],'predefined_favorable_signal':False,'reason':'Más cases cumplen cuatro obligaciones en treatment, pero aparece desviación de contrato en E03; formato treatment0/6. Resultado mixto, sin mejora fiable/general acreditada.','model_calls_cumulative':15,'estimated_api_cost_usd_cumulative':json.loads((run/'round-status.json').read_text())['cumulative_estimated_api_cost_usd'],'budget_limit_usd_cumulative':0.20,'foundry_promotions':0,'notes':['Formato y contenido no son una métrica compuesta; content pass es juicio local no independiente.','E01baseline ya visto en intento fallido; no completamente inédito.','Una repetición/seis cases; no variabilidad estadística.','Reference path checks diagnósticos se separan de soporte semántico y JSON raw inválido.']}
for condition in ['baseline','treatment']:
 rr=[r for r in rows if r['condition']==condition]
 summary['counts'][condition]={'raw_format_pass':sum(r['raw_format_pass'] for r in rr),'diagnostic_status_matches':sum(r['diagnostic_status_matches'] for r in rr),'rubric_content_pass':sum(r['rubric_content_pass'] for r in rr),'false_blocks_on_coherent':sum(r['false_block_on_coherent'] for r in rr),'reference_paths_exist_diagnostic':sum(r['reference_paths_exist_diagnostic'] for r in rr),'scope_contract_deviations':sum(r['scope_contract_deviation'] for r in rr)}
write(run/'evaluation-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False,indent=2))
