"""Verifica fixtures y separación de payloads. No llama modelos ni puntúa sus respuestas."""
from pathlib import Path
import csv,hashlib,io,itertools,json

ROOT=Path(__file__).resolve().parent

def read(rel):return json.loads((ROOT/rel).read_text(encoding='utf-8'))
def sha_text(text):return hashlib.sha256(text.encode()).hexdigest()

def verify():
    index=read('reviewer/case-index.json')
    assert [r['case_id'] for r in index]==['E01','E02','E03','E04','E05','E06']
    assert sorted(r['family'] for r in index)==['freeze','freeze','labels','labels','reproduction','reproduction']
    assert sum(r['kind']=='defect' for r in index)==3
    baseline=(ROOT/'conditions/baseline/workflow.md').read_text()
    treatment=(ROOT/'conditions/treatment/workflow.md').read_text()
    supplement=(ROOT/'conditions/treatment/supplement.md').read_text()
    assert treatment.replace(supplement,'',1)==baseline
    assert treatment.count(supplement)==1
    # Reconstruir cada payload solo desde las fuentes públicas; expected no entra.
    common=(ROOT/'common/task-contract.txt').read_text()
    for entry in index:
        cid=entry['case_id'];task=(ROOT/f'agent_inputs/{cid}/task.md').read_text().rstrip('\n')
        context=read(f'agent_inputs/{cid}/context.json');artifacts=read(f'agent_inputs/{cid}/artifacts.json')
        expected=read(entry['expected_path'])
        assert expected['status']==('MUST_CORRECT' if entry['kind']=='defect' else 'READY')
        assert len(expected['required'])==4 and len(expected['forbidden'])==2
        for branch,rules in [('baseline',baseline),('treatment',treatment)]:
            assembled=common+'\n## Pautas de trabajo\n\n'+rules+'\n## Tarea\n\n'+task+'\n\n## Contexto\n\n'+json.dumps(context,ensure_ascii=False,indent=2)+'\n\n## Artifacts del expediente\n\n'+json.dumps(artifacts,ensure_ascii=False,indent=2)+'\n'
            assert (ROOT/f'payloads/{cid}/{branch}.txt').read_text()==assembled
    freeze_results=[]
    for cid in ('E01','E02'):
        art=read(f'agent_inputs/{cid}/artifacts.json')
        manifest=json.loads(art['reports/manifest-01.json']);approval=art['reports/approval-01.json']
        assert sha_text(art['reports/manifest-01.json'])==approval['manifest_sha256']
        entry=manifest['files'][0];matches=sha_text(art[entry['path']])==entry['sha256']
        assert matches==(cid=='E02')
        if cid=='E01':assert sha_text(art['reports/archive/plan-original.md'])==entry['sha256']
        else:assert sha_text(art['analysis/plan.md'])!=entry['sha256']
        oracle=read(f'reviewer/expected/{cid}.json')['facts']
        if cid=='E01':
            assert oracle['old_plan_sha256']==entry['sha256']
            assert oracle['new_plan_sha256']==sha_text(art['analysis/plan.md'])
            assert oracle['approval_manifest_sha256']==approval['manifest_sha256']
        else:
            assert oracle['frozen_plan_sha256']==entry['sha256']
            assert oracle['live_plan_sha256']==sha_text(art['analysis/plan.md'])
        freeze_results.append({'case_id':cid,'manifest_file_hash_matches':matches,'approval_reference_matches':True})
    art=read('agent_inputs/E03/artifacts.json');source=art['data/source.json']
    # Ejercer la frontera real: writer .1f y reader float, no solo comparar strings.
    buf=io.StringIO(newline='');writer=csv.DictWriter(buf,fieldnames=['case_id','duration_minutes']);writer.writeheader()
    writer.writerows({'case_id':r['case_id'],'duration_minutes':format(r['duration_minutes'],'.1f')} for r in source)
    buf.seek(0);persisted=[{'case_id':r['case_id'],'duration_minutes':float(r['duration_minutes'])} for r in csv.DictReader(buf)]
    assert persisted==art['runs/original/execution.json']['consumed_values']
    original=[r['case_id'] for r in persisted if r['duration_minutes']>=15.0]
    memory=[r['case_id'] for r in source if r['duration_minutes']>=15.0]
    oracle=read('reviewer/expected/E03.json')['facts']
    assert original==oracle['original_selected_ids']==['Q-17']
    assert memory==oracle['reproduction_selected_ids']==[]
    assert all(abs(a['duration_minutes']-b['duration_minutes'])<=0.1 for a,b in zip(persisted,source))
    art=read('agent_inputs/E04/artifacts.json')
    a,b=art['runs/original/data.json'],art['runs/reproduction/data.json']
    assert a!=b and json.loads(a)==json.loads(b)
    oracle=read('reviewer/expected/E04.json')['facts']
    assert oracle['same_parsed_rows'] is True and oracle['same_bytes'] is False
    assert oracle['selected_queues']==['A']
    assert [r['queue'] for r in json.loads(a) if r['tickets']>=10]==['A']
    assert all(type(r['tickets']) is int for r in json.loads(b))
    label_checks=[]
    for cid in ('E05','E06'):
        art=read(f'agent_inputs/{cid}/artifacts.json');rows=art['analysis/weekly.json']
        oracle=read(f'reviewer/expected/{cid}.json')['facts']
        for ordered in itertools.permutations(rows):
            candidates=[r for r in ordered if r['population']=='Norte' and r['metric']=='on_time_share' and r['complete']]
            selected=max(candidates,key=lambda r:r['week_start'])
            assert selected['week_start']==oracle['week_start']=='2025-10-20'
            assert selected['week_end_exclusive']==oracle['week_end_exclusive']=='2025-10-27'
            assert selected['on_time']/selected['deliveries']==oracle['share']==0.92
        label_checks.append({'case_id':cid,'orders_checked':24,'share':0.92,'week_start':'2025-10-20'})
    prep=read('preparation.json');assert prep['model_calls']==0 and prep['execution_authorized'] is False
    result={'status':'PASS','verification_scope':'Preparación y consistencia de fixtures; no resultados de modelos','cases':6,'condition_payloads':12,'defect_cases':3,'coherent_cases':3,'payload_expected_sources_excluded':True,'conditions_differ_only_in_three_sections':True,'freeze_fixtures':freeze_results,'serialization_counterexample_verified':True,'JSON_whitespace_semantic_equivalence_verified':True,'labels_permutations':label_checks,'model_calls':0,'api_cost_usd':0,'runtime_isolation_verified':False}
    manifest=ROOT/'evidence-manifest-01.json'
    if manifest.exists():
        m=json.loads(manifest.read_text())
        assert all(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in m['files'])
        print('Manifest congelado verificado.',file=__import__('sys').stderr)
    return result

if __name__=='__main__':
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
