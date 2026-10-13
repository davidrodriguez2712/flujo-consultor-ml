"""Verifica preparación y fixtures. No llama modelos ni evalúa respuestas."""
from pathlib import Path
import csv,difflib,hashlib,io,json
ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
def read(rel):return json.loads((ROOT/rel).read_text())
def text(rel):return (ROOT/rel).read_text()
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def verify():
    index=read('reviewer/case-index.json')
    assert [e['case_id'] for e in index]==['D01','D02','D03','D04']
    assert sum(e['draft_requested'] for e in index)==3
    assert [e['format'] for e in index]==['json','markdown','json','json']
    baseline=text('conditions/baseline/workflow.md');treatment=text('conditions/treatment/workflow.md');supplement=text('conditions/treatment/supplement.txt')
    assert treatment.count(supplement)==1 and treatment.replace(supplement,'',1)==baseline
    source=read('conditions/source.json')
    for branch,content in [('baseline',baseline),('treatment',treatment)]:assert hashlib.sha256(content.encode()).hexdigest()==source[branch]['sha256']
    assert text('conditions/workflow.diff')==''.join(difflib.unified_diff(baseline.splitlines(True),treatment.splitlines(True),fromfile='baseline/workflow.md',tofile='treatment/workflow.md'))
    common=text('common/task-contract.txt');sizes=[]
    for entry in index:
        cid=entry['case_id'];expected=read(entry['expected_path'])
        assert expected['status']=='READY' and expected['draft_requested']==entry['draft_requested']
        assert len(expected['required'])==(6 if entry['draft_requested'] else 4) and len(expected['forbidden'])==3
        context=read(f'agent_inputs/{cid}/context.json');artifacts=read(f'agent_inputs/{cid}/artifacts.json');task=text(f'agent_inputs/{cid}/task.md').rstrip('\n')
        assert context['requested_action']==('draft_task' if entry['draft_requested'] else 'follow_up_only')
        for branch,rules in [('baseline',baseline),('treatment',treatment)]:
            payload=common+'\n## Pautas\n\n'+rules+'\n## Tarea\n\n'+task+'\n\n## Contexto\n\n'+json.dumps(context,ensure_ascii=False,indent=2)+'\n\n## Artifacts\n\n'+json.dumps(artifacts,ensure_ascii=False,indent=2)+'\n'
            assert text(f'payloads/{cid}/{branch}.txt')==payload
            sizes.append({'case':cid,'condition':branch,'utf8_bytes':len(payload.encode())})
    a=read('agent_inputs/D01/artifacts.json');m=a['data/inventory-metadata.json'];facts=read('reviewer/expected/D01.json')['facts']
    assert m['sku_count']*m['complete_weeks']==m['described_rows']==facts['expected_rows_from_metadata']==520
    assert m['raw_access']==facts['raw_access']=='PENDING'
    assert a['intake/request.json']['owner_name'] is None and a['intake/request.json']['deadline'] is None
    assert a['decisions/open.json']['metric_and_acceptance_threshold']=='PENDING'
    a=read('agent_inputs/D02/artifacts.json');rows=list(csv.DictReader(io.StringIO(a['data/readings.csv'])))
    assert len(rows)==read('reviewer/expected/D02.json')['facts']['rows']==3
    assert [float(r['temperature_c']) for r in rows]==[41,58,44]
    assert a['data/dictionary.json']['labels_available'] is False
    assert a['intake/request.json']['approved_thresholds'] is None and a['intake/request.json']['reviewer_name'] is None
    a=read('agent_inputs/D03/artifacts.json')
    assert a['constraints/access.json']['private_tickets']=='PENDING_APPROVAL'
    assert a['constraints/access.json']['provider_api_calls']=='NOT_AUTHORIZED'
    assert a['constraints/access.json']['evaluation_thresholds']=='PENDING'
    assert a['solution/status.json']['existing_eval_results'] is None
    a=read('agent_inputs/D04/artifacts.json');facts=read('reviewer/expected/D04.json')['facts']
    assert len(a['intake/questions.json']['open'])==facts['follow_up_actions']==facts['open_questions']==3
    assert a['project/state.json']['data_access']==facts['data_access']=='PENDING'
    assert 'Redactar task en esta respuesta' in a['constraints/scope.json']['not_authorized']
    old=WORKSPACE/'evaluations/os-workflow/2026-10-09-less-guided-01';transfer=WORKSPACE/'evaluations/os-workflow/2026-10-09-transfer-01'
    manifests=[old/'evidence-manifest-01.json',old/'execution-config-01/execution-manifest-01.json',old/'execution-config-02/execution-manifest-02.json',old/'runs/round-01/run-manifest-01.json',old/'runs/round-02/run-manifest-02.json',WORKSPACE/'pilots/retail-capacidad-semanal-publico/reports/package/evidence-manifest-01.json',WORKSPACE/'artifacts/os-workflow-refinement-2026-10-09/change-manifest-01.json',transfer/'evidence-manifest-01.json',transfer/'execution-config-01/execution-manifest-01.json',transfer/'runs/round-01/run-manifest-01.json',WORKSPACE/'evaluations/os-workflow/2026-10-09-local-refinement-02/change-manifest-02.json']
    historical=[]
    for path in manifests:
        base=WORKSPACE/'pilots/retail-capacidad-semanal-publico' if 'pilots' in path.parts else path.parent
        manifest=json.loads(path.read_text())
        for row in manifest['files']:assert sha(base/row['path'])==row['sha256'],str(base/row['path'])
        historical.append({'manifest':str(path.relative_to(WORKSPACE)),'files':len(manifest['files']),'status':'PASS'})
    prep=read('preparation.json');assert prep['model_calls']==0 and prep['paid_execution_authorized'] is False
    assert read('design-approval.json')['paid_execution_authorized'] is False
    frozen=ROOT/'evidence-manifest-01.json'
    if frozen.exists():
        for row in json.loads(frozen.read_text())['files']:assert sha(ROOT/row['path'])==row['sha256']
    return {'status':'PASS_LOCAL_PREPARATION','cases':4,'draft_cases':3,'control_cases':1,'public_only_payloads':8,'only_one_paragraph_differs':True,'fixture_checks':['520 descriptive rows from metadata, no actual raw present','Three readings parsed, no labels/approved thresholds','RAG access/API restrictions and no eval results','Three follow-up questions and no task request'],'historical_integrity':historical,'historical_files_intact':sum(e['files'] for e in historical),'payload_sizes':sizes,'agent_calls':0,'api_cost_usd':0,'independent_review':False,'runtime_isolation_verified':False,'semantic_effectiveness':'NOT_EVALUATED'}
if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
