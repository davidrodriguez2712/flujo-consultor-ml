"""Pruebas del wrapper final con fixtures manuales, sin métricas del holdout real."""
import csv
import hashlib
import importlib.util
import json
from pathlib import Path
import pytest
MODULE=Path(__file__).with_name('credit_final.py')
BASE=Path(__file__).with_name('credit_baseline.py')

def code():
    assert MODULE.is_file(), 'Falta implementar credit_final'
    spec=importlib.util.spec_from_file_location('credit_final_under_test',MODULE)
    c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c);return c

def write_table(root,name,rows):
    raw=root/'data/raw';raw.mkdir(parents=True,exist_ok=True)
    with (raw/(name+'.csv')).open('w',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)

def fixture(root):
    apps=[];history=[];outcomes=[];decisions=[];post=[]
    for identifier,customer,scoring,status,target,available,bureau in [
        ('T1','C1','2024-01-01','observed','0','2024-04-08','800'),
        ('T2','C2','2024-02-01','observed','1','2024-05-09','400'),
        ('LATE','C3','2025-06-01','observed','FUTURE_POISON','2025-09-07','600'),
        ('A','C1','2025-07-02','observed','0','2025-10-08','750'),
        ('B','C4','2025-08-02','observed','1','2025-11-08','450'),
        ('R','C5','2025-09-02','not_observed_rejected','','','500')]:
        apps.append(dict(application_id=identifier,customer_id=customer,scoring_at=scoring,monthly_income='2000',debt_to_income='.2',requested_amount='5000',bureau_score=bureau))
        history.append(dict(application_id=identifier,customer_id=customer,available_at=scoring,prior_late_count='0'))
        outcomes.append(dict(application_id=identifier,label_status=status,label_available_at=available,target_30dpd_90d=target))
        decisions.append(dict(application_id=identifier,decision='rejected' if identifier=='R' else 'approved'))
        post.append(dict(application_id=identifier,max_dpd_90d='LEAKAGE_POISON'))
    for name,rows in [('applications',apps),('history',history),('outcomes',outcomes),('decisions',decisions),('post_decision',post)]:write_table(root,name,rows)
    return root

def freeze(c,root):
    path=root/'freeze.json'
    path.write_text(json.dumps({'runner_sha256':hashlib.sha256(MODULE.read_bytes()).hexdigest(),'baseline_sha256':hashlib.sha256(BASE.read_bytes()).hexdigest(),'policy':c.POLICY,'inputs':{'data/raw/'+p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (root/'data/raw').glob('*.csv')}}))
    return path

def test_train_filters_late_labels_before_interpreting_target(tmp_path):
    c=code();fixture(tmp_path)
    rows=c.load_train(tmp_path)
    assert [r['application_id'] for r in rows]==['T1','T2']
    assert [r['target'] for r in rows]==[0,1]

def test_scoring_does_not_load_outcomes_or_postdecision_features(tmp_path):
    c=code();fixture(tmp_path)
    (tmp_path/'data/raw/outcomes.csv').unlink()
    rows=c.load_scoring(tmp_path)
    assert [r['application_id'] for r in rows]==['A','B','R']
    assert all('target' not in r and 'max_dpd_90d' not in r and 'decision' not in r for r in rows)

def test_labels_available_at_evaluation_timestamp_and_missing_are_not_zero(tmp_path):
    c=code();fixture(tmp_path)
    labels=c.load_labels(tmp_path,{'A','B','R'})
    assert labels['A']['target']==0 and labels['B']['target']==1
    assert labels['R']['target'] is None and labels['R']['label_status']=='not_observed_rejected'
    with (tmp_path/'data/raw/outcomes.csv').open(newline='') as stream: data=list(csv.DictReader(stream))
    for r in data:
        if r['application_id']=='B':r['label_available_at']='2026-01-16';r['target_30dpd_90d']='UNAVAILABLE_POISON'
    write_table(tmp_path,'outcomes',data)
    labels=c.load_labels(tmp_path,{'B'})
    assert labels['B']['target'] is None and labels['B']['label_status']=='pending'

def test_full_runner_scores_all_requests_but_evaluates_only_complete_labels(tmp_path):
    c=code();fixture(tmp_path);f=freeze(c,tmp_path)
    result=c.run(tmp_path,tmp_path/'output',f)
    assert result['training_rows']==2 and result['scored_rows']==3 and result['evaluated_rows']==2
    assert result['reference_probability']==.5
    detail=json.loads((tmp_path/'output/results.json').read_text())
    assert detail['evaluable']['model']['rows']==2
    assert detail['evaluable']['model']['roc_auc']==1
    assert detail['all_applications_monthly']['2025-09']['precision'] is None
    assert detail['all_applications_monthly']['2025-09']['label_coverage_selected']==0
    assert detail['evaluable']['customer_segments']['known']['model']['rows']==1
    assert detail['evaluable']['customer_segments']['new']['model']['rows']==1
    events=json.loads((tmp_path/'output/metadata.json').read_text())['events']
    assert events.index('predictions_persisted')<events.index('evaluation_labels_loaded')
    with pytest.raises(FileExistsError):c.run(tmp_path,tmp_path/'output',f)

@pytest.mark.parametrize('filename',['history.csv','outcomes.csv'])
def test_run_refuses_changed_inputs_without_writing_results(tmp_path,filename):
    c=code();fixture(tmp_path);f=freeze(c,tmp_path)
    with (tmp_path/'data/raw'/filename).open('a') as stream:stream.write('\n')
    with pytest.raises(ValueError,match='hash'):c.run(tmp_path,tmp_path/'output',f)
    assert not (tmp_path/'output').exists()

def test_run_refuses_changed_policy(tmp_path):
    c=code();fixture(tmp_path);f=freeze(c,tmp_path)
    data=json.loads(f.read_text());data['policy']['training_cutoff']='2025-07-02';f.write_text(json.dumps(data))
    with pytest.raises(ValueError,match='policy'):c.run(tmp_path,tmp_path/'output',f)
    assert not (tmp_path/'output').exists()

def test_duplicate_join_key_is_rejected(tmp_path):
    c=code();fixture(tmp_path)
    with (tmp_path/'data/raw/history.csv').open(newline='') as stream:rows=list(csv.DictReader(stream))
    write_table(tmp_path,'history',rows+[rows[0]])
    with pytest.raises(ValueError,match='duplicad'):c.load_scoring(tmp_path)

def test_labels_must_match_requested_application_ids(tmp_path):
    c=code();fixture(tmp_path)
    with pytest.raises(ValueError,match='label'):c.load_labels(tmp_path,{'ABSENT'})
