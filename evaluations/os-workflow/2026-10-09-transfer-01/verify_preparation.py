"""Checks de preparación y oracles sintéticos. No invoca modelos ni puntúa outputs."""
from pathlib import Path
import csv, hashlib, io, json, difflib

ROOT=Path(__file__).resolve().parent
WORKSPACE=ROOT.parents[2]
def read(rel): return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def text(rel): return (ROOT/rel).read_text(encoding='utf-8')
def sha(value): return hashlib.sha256(value).hexdigest()
def text_sha(value): return sha(value.encode('utf-8'))

def verify():
    index=read('reviewer/case-index.json')
    assert [r['case_id'] for r in index]==['T01','T02','T03','T04','T05','T06']
    assert sorted(r['family'] for r in index)==['continuity','continuity','format','format','reproduction','reproduction']
    assert sum(r['format']=='json' for r in index)==5
    assert sum(r['format']=='markdown' for r in index)==1
    source=read('conditions/source.json')
    branches={b:text(f'conditions/{b}/workflow.md') for b in ('baseline','treatment')}
    for branch in branches:
        assert text_sha(branches[branch])==source[branch]['sha256']
        # La comprobación de referencia fuente es separada del freeze del paquete.
        assert sha((WORKSPACE/source[branch]['path']).read_bytes())==source[branch]['sha256']
    assert text('conditions/workflow.diff')==''.join(difflib.unified_diff(branches['baseline'].splitlines(True),branches['treatment'].splitlines(True),fromfile='baseline/workflow.md',tofile='treatment/workflow.md'))
    common=text('common/task-contract.txt')
    sizes=[]
    for entry in index:
        cid=entry['case_id']; task=text(f'agent_inputs/{cid}/task.md').rstrip('\n')
        context=read(f'agent_inputs/{cid}/context.json'); artifacts=read(f'agent_inputs/{cid}/artifacts.json')
        expected=read(entry['expected_path'])
        assert len(expected['required'])==4 and len(expected['forbidden'])==2
        assert expected['family']==entry['family'] and expected['format']==entry['format']
        assert expected['status']==('MUST_CORRECT' if cid in ('T03','T06') else 'READY')
        for branch,rules in branches.items():
            assembled=common+'\n## Pautas de trabajo\n\n'+rules+'\n## Tarea\n\n'+task+'\n\n## Contexto\n\n'+json.dumps(context,ensure_ascii=False,indent=2)+'\n\n## Artifacts del expediente\n\n'+json.dumps(artifacts,ensure_ascii=False,indent=2)+'\n'
            actual=text(f'payloads/{cid}/{branch}.txt')
            assert actual==assembled
            sizes.append({'case_id':cid,'condition':branch,'utf8_bytes':len(actual.encode('utf-8'))})
    art=read('agent_inputs/T01/artifacts.json');contract=art['contracts/shortlist.json']
    selected=[r['customer_id'] for r in sorted(art['analysis/scores.json'],key=lambda r:(-r['score'],r['customer_id'])) if r['score']>=contract['minimum_score']][:contract['capacity']]
    assert selected==art['plans/shortlist.json']['customer_ids']==read('reviewer/expected/T01.json')['facts']['selected_ids']
    art=read('agent_inputs/T02/artifacts.json');s=art['analysis/scenario.json'];facts=read('reviewer/expected/T02.json')['facts']
    base=s['baseline']['gross_profit']/s['baseline']['revenue']; scenario=s['scenario']['gross_profit']/s['scenario']['revenue']
    assert base==facts['baseline_margin'] and scenario==facts['scenario_margin']
    assert abs((scenario-base)*100-facts['difference_percentage_points'])<1e-12
    art=read('agent_inputs/T03/artifacts.json');rows=art['data/source.json']
    # Frontera original ejercida realmente: CSV preserva texto, reader convierte int.
    buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=['product_id','stock']);writer.writeheader();writer.writerows(rows)
    buf.seek(0);consumed=[{'product_id':int(r['product_id']),'stock':int(r['stock'])} for r in csv.DictReader(buf)]
    catalog={r['product_id']:r['reorder_point'] for r in art['data/catalog.json']}
    def match_and_select(data):
        matched=[r for r in data if r['product_id'] in catalog]
        return len(matched),[r['product_id'] for r in matched if r['stock']<catalog[r['product_id']]]
    facts=read('reviewer/expected/T03.json')['facts']
    for data,run_key,match_key,selected_key in [(consumed,'runs/original/result.json','original_matches','original_selected_ids'),(rows,'runs/reproduction/result.json','reproduction_matches','reproduction_selected_ids')]:
        matched,selected=match_and_select(data)
        assert matched==art[run_key]['matched_rows']==facts[match_key]
        assert selected==art[run_key]['selected_ids']==facts[selected_key]
        assert [r['product_id'] for r in data]==art[run_key]['consumed_ids']
    art=read('agent_inputs/T04/artifacts.json');weeks=art['data/weeks.json'];facts=read('reviewer/expected/T04.json')['facts']
    persisted=json.loads(json.dumps(weeks))
    gross=sum(r['sales_units'] for r in persisted)/len(persisted)
    net=[r['sales_units']-r['returned_units'] for r in persisted]
    assert gross==art['runs/v1/output.json']['forecast']==facts['v1_forecast']==120
    assert net==facts['net_series'] and sum(net)/len(net)==facts['v2_forecast']==100
    assert art['decisions/change-02.json']['status']=='APPROVED'
    assert len(set(art['decisions/change-02.json']['destinations']))==2
    art=read('agent_inputs/T05/artifacts.json');m=json.loads(art['reports/manifest-01.json']);facts=read('reviewer/expected/T05.json')['facts']
    for row in m['files']:assert text_sha(art[row['path']])==row['sha256']
    assert text_sha(art['reports/manifest-01.json'])==art['reports/approval-01.json']['manifest_sha256']==facts['approval_manifest_sha256']
    assert text_sha(art['reports/frozen-01/plan.md'])==facts['frozen_plan_sha256']
    assert text_sha(art['analysis/plan.md'])==facts['live_plan_sha256']!=facts['frozen_plan_sha256']
    assert len(art['requests/task-draft.json']['dependencies'])==facts['execution_dependencies_pending']==2
    art=read('agent_inputs/T06/artifacts.json');facts=read('reviewer/expected/T06.json')['facts']
    assert all(art['campaign/state.json'][key]=='PENDING' for key in facts['pending'])
    assert art['campaign/state.json']['send_status']==facts['send_status']=='NOT_STARTED'
    assert len(art['campaign/contract.json']['required_before_send'])==2
    assert art['campaign/contract.json']['allowed_preparation'] and facts['preparation_allowed'] is True
    old=WORKSPACE/'evaluations/os-workflow/2026-10-09-less-guided-01'
    manifests=[old/'evidence-manifest-01.json',old/'execution-config-01/execution-manifest-01.json',old/'execution-config-02/execution-manifest-02.json',old/'runs/round-01/run-manifest-01.json',old/'runs/round-02/run-manifest-02.json',WORKSPACE/'pilots/retail-capacidad-semanal-publico/reports/package/evidence-manifest-01.json',WORKSPACE/'artifacts/os-workflow-refinement-2026-10-09/change-manifest-01.json']
    verified=[]
    for path in manifests:
        manifest=json.loads(path.read_text());base=path.parent
        # Manifest del piloto usa rutas relativas a raíz del proyecto, no package/.
        if 'pilots' in path.parts:base=WORKSPACE/'pilots/retail-capacidad-semanal-publico'
        for row in manifest['files']:
            target=base/row['path']
            assert sha(target.read_bytes())==row['sha256'],str(target)
        verified.append({'manifest':str(path.relative_to(WORKSPACE)),'files':len(manifest['files']),'status':'PASS'})
    prep=read('preparation.json');assert prep['model_calls']==0 and prep['execution_authorized'] is False
    assert read('design-approval.json')['execution_authorized'] is False
    frozen=ROOT/'evidence-manifest-01.json'
    if frozen.exists():
        for row in json.loads(frozen.read_text())['files']:assert sha((ROOT/row['path']).read_bytes())==row['sha256']
    return {'status':'PASS','scope':'Consistencia de preparación y fixtures, no evaluación de agentes','cases':6,'payloads':12,'json_contracts':5,'markdown_contracts':1,'public_only_payload_reconstruction':True,'oracles_verified':['shortlist','margins','CSV-int-join','gross-net-forecast','historical-freeze','launch-dependencies'],'historical_integrity':verified,'historical_files_verified':sum(r['files'] for r in verified),'payload_sizes':sizes,'model_calls':0,'api_cost_usd':0,'runtime_isolation_verified':False,'semantic_effectiveness':'NOT_EVALUATED'}

if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
