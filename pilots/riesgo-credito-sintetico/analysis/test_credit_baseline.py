"""Regresiones del baseline: disponibilidad, aislamiento y métricas comprobables."""
import copy
import csv
import importlib.util
from pathlib import Path
import pytest
MODULE=Path(__file__).with_name('credit_baseline.py')

def code():
    assert MODULE.is_file(), 'Falta implementar credit_baseline'
    spec=importlib.util.spec_from_file_location('credit_baseline_under_test',MODULE)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module

def row(identifier='A',target=0,**changes):
    sample=dict(application_id=identifier,customer_id='C1',scoring_at='2024-06-01',history_available_at='2024-05-30',label_available_at='2024-09-07',label_status='observed',target=target,monthly_income='2000',debt_to_income='0.2',requested_amount='5000',bureau_score='650',prior_late_count='0')
    sample.update(changes);return sample

@pytest.mark.parametrize('changes',[
    {'label_available_at':'2025-01-02'}, {'scoring_at':'2025-01-01'},
    {'label_status':'pending','target':None},{'target':True},
    {'history_available_at':'2024-06-02'}, {'debt_to_income':'nan'}])
def test_fit_rejects_unavailable_or_invalid_training_inputs(changes):
    with pytest.raises(ValueError):code().fit([row(**changes)],'2025-01-01')

def test_exact_cutoff_label_is_admissible_and_prediction_ignores_outcomes():
    c=code();model=c.fit([row(label_available_at='2025-01-01'),row('B',1,bureau_score='500')],'2025-01-01')
    original=c.predict(model,[row()])[0]['score']
    changed=row('Z',1,customer_id='OTHER',max_dpd_90d=90,decision='rejected',funded_amount=999999)
    assert c.predict(model,[changed])[0]['score']==original

def test_predict_does_not_fit_preprocessing_or_require_labels():
    c=code();model=c.fit([row(monthly_income='1000'),row('B',1,monthly_income='3000')],'2025-01-01')
    assert model['means']['monthly_income']==2000
    before=copy.deepcopy(model)
    future=row('Z',monthly_income='9999');future.pop('target');future.pop('label_available_at');future.pop('label_status')
    assert 0<c.predict(model,[future])[0]['score']<1
    assert model==before

def test_numeric_baseline_learns_without_identifier_features():
    c=code();train=[row(str(i),int(i>=10),bureau_score=str(800 if i<10 else 400)) for i in range(20)]
    model=c.fit(train,'2025-01-01');scores=c.predict(model,[row('LOW',bureau_score='800'),row('HIGH',bureau_score='400')])
    assert scores[0]['score']<.3 and scores[1]['score']>.7
    assert model['reference_probability']==.5

def test_hand_checked_brier_and_auc_with_ties():
    c=code();rows=[row('A',0),row('B',1),row('C',1)]
    scores=[{'application_id':'A','score':.5},{'application_id':'B','score':.5},{'application_id':'C','score':1.0}]
    actual=c.metrics(scores,rows)
    assert actual['brier_score']==pytest.approx(1/6)
    assert actual['roc_auc']==.75
    assert actual['calibration'][-1]['rows']==1

@pytest.mark.parametrize('targets',[[],[0,0],[1,1]])
def test_auc_requires_both_classes_and_empty_metrics_are_undefined(targets):
    c=code();rows=[row(str(i),v) for i,v in enumerate(targets)]
    actual=c.metrics([{'application_id':r['application_id'],'score':.5} for r in rows],rows)
    assert actual['roc_auc'] is None
    if not targets: assert actual['brier_score'] is None

def test_tied_ranking_capacity_and_label_coverage():
    c=code();rows=[row('B',0),row('A',1),row('C',1)]
    scores=[{'application_id':'B','score':.9},{'application_id':'A','score':.9},{'application_id':'C','score':.1}]
    actual=c.selection(scores,rows,2)
    assert actual['selected_ids']==['A','B']
    assert actual['precision']==.5 and actual['recall']==.5 and actual['lift']==.75
    missing=[row('B',None,label_status='pending'),row('A',1),row('C',1)]
    actual=c.selection(scores,missing,2)
    assert actual['label_coverage_selected']==.5
    assert actual['precision'] is None and actual['recall'] is None and actual['lift'] is None

def test_zero_capacity_and_no_positive_metrics():
    c=code();scores=[{'application_id':'A','score':.5}]
    result=c.selection(scores,[row()],100)
    assert result['k_effective']==1 and result['precision']==0 and result['recall'] is None and result['lift'] is None
    result=c.selection(scores,[row()],0)
    assert result['precision'] is None and result['label_coverage_selected'] is None

@pytest.mark.parametrize('scores',[
    [{'application_id':'A','score':float('nan')}],
    [{'application_id':'Z','score':.1}],
    [{'application_id':'A','score':1.1}],
    [{'application_id':'A','score':.1},{'application_id':'A','score':.2}],
])
def test_metrics_reject_invalid_scores_or_alignment(scores):
    with pytest.raises(ValueError):code().metrics(scores,[row()])

def test_metrics_refuse_missing_targets():
    with pytest.raises(ValueError):code().metrics([{'application_id':'A','score':.1}],[row(target=None,label_status='pending')])

def test_development_loader_filters_future_targets_before_parsing(tmp_path):
    c=code();genpath=Path(__file__).with_name('generate_synthetic_data.py')
    spec=importlib.util.spec_from_file_location('credit_gen',genpath);gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    raw=tmp_path/'data/raw';gen.generate(raw)
    path=raw/'outcomes.csv'
    with path.open(newline='') as stream: records=list(csv.DictReader(stream));fields=list(records[0])
    for record in records:
        if record['application_id']=='A005401':record['target_30dpd_90d']='FUTURE_POISON'
    with path.open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=fields);writer.writeheader();writer.writerows(records)
    # La prueba del filtro usa directamente el loader; run verifica hashes además.
    data=c.load_development(tmp_path)
    assert len(data)==1546
    assert all(r['scoring_at']<'2025-03-01' for r in data)


def test_loader_rejects_duplicate_application_join_keys(tmp_path):
    c=code();genpath=Path(__file__).with_name('generate_synthetic_data.py')
    spec=importlib.util.spec_from_file_location('credit_gen2',genpath);gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    raw=tmp_path/'data/raw';gen.generate(raw)
    with (raw/'history.csv').open(newline='') as stream: records=list(csv.DictReader(stream));fields=list(records[0])
    with (raw/'history.csv').open('a',newline='') as stream:csv.DictWriter(stream,fieldnames=fields).writerow(records[0])
    with pytest.raises(ValueError,match='duplicad'):c.load_development(tmp_path)

def fixture_project(tmp_path):
    genpath=Path(__file__).with_name('generate_synthetic_data.py')
    spec=importlib.util.spec_from_file_location('credit_gen_run',genpath);gen=importlib.util.module_from_spec(spec);spec.loader.exec_module(gen)
    gen.generate(tmp_path/'data/raw')
    return tmp_path

def freeze_file(c,root):
    import hashlib,json
    files={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'data/raw').glob('*.csv')}
    path=root/'freeze.json'
    path.write_text(json.dumps({'code_sha256':hashlib.sha256(MODULE.read_bytes()).hexdigest(),'policy':c.POLICY,'inputs':files}))
    return path

def test_development_run_matches_reference_population_and_does_not_evaluate_final(tmp_path):
    c=code();root=fixture_project(tmp_path);freeze=freeze_file(c,root)
    summary=c.run(root,root/'result',freeze)
    assert summary['training_rows']==1248 and summary['validation_rows']==298
    assert summary['reference_probability']==pytest.approx(134/1248)
    assert summary['final_metrics_computed'] is False
    assert (root/'result/model.json').is_file()
    import json
    detail=json.loads((root/'result/results.json').read_text())
    assert set(detail['customer_segments'])=={'known','new'}
    assert sum(r['model']['rows'] for r in detail['customer_segments'].values())==298
    assert sum(r['model']['rows'] for r in detail['monthly'].values())==298
    assert summary['brier_reference'] is not None
    with pytest.raises(FileExistsError):c.run(root,root/'result',freeze)

def test_run_refuses_changed_input_before_writing_output(tmp_path):
    c=code();root=fixture_project(tmp_path);freeze=freeze_file(c,root)
    with (root/'data/raw/history.csv').open('a') as stream:stream.write('\n')
    with pytest.raises(ValueError,match='hash'):c.run(root,root/'result',freeze)
    assert not (root/'result').exists()


def test_reporting_separates_months_and_known_vs_new_clients():
    c=code()
    train=[row('T',customer_id='C1')]
    val=[row('A',0,customer_id='C1',scoring_at='2025-01-03'),row('B',1,customer_id='C2',scoring_at='2025-02-03')]
    scores=[{'application_id':'A','score':.2},{'application_id':'B','score':.2}]
    reference=[{'application_id':'A','score':.5},{'application_id':'B','score':.5}]
    actual=c.group_reports(scores,reference,train,val)
    assert actual['customer_segments']['known']['model']['rows']==1
    assert actual['customer_segments']['known']['model']['brier_score']==pytest.approx(.04)
    assert actual['customer_segments']['new']['model']['brier_score']==pytest.approx(.64)
    assert actual['customer_segments']['new']['reference']['brier_score']==.25
    assert actual['monthly']['2025-01']['model']['positive_rate']==0
    assert actual['monthly']['2025-02']['model']['positive_rate']==1
    assert actual['monthly']['2025-02']['selection']['selected_ids']==['B']
