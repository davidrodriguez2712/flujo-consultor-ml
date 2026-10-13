import sys
from pathlib import Path
import pytest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from forecast import build_weekly, forecasts, metrics, choose_method


def row(invoice='A',date='2010-01-05 09:00:00',**kw):
    return {'invoice_id':invoice,'invoice_at':date,'quantity':'1','unit_price':'2','country':'United Kingdom',**kw}


def test_weekly_unique_invoices_filters_and_partial_boundaries():
    rows=[row('first','2010-01-01 09:00:00'),row(),row(),row('B'),row('C9'),row('X',country='France'),row('N',quantity='-1'),row('Z',unit_price='0'),row('last','2010-01-20 09:00:00')]
    weekly,audit=build_weekly(rows)
    assert weekly==[{'cutoff':'2010-01-04','week_end_exclusive':'2010-01-11','actual':2},{'cutoff':'2010-01-11','week_end_exclusive':'2010-01-18','actual':0}]
    assert audit['raw_rows']==9


def test_empty_source_is_rejected():
    with pytest.raises(ValueError):build_weekly([])


def weekly():
    return [{'cutoff':f'2010-02-{day:02d}','week_end_exclusive':f'2010-02-{day+7:02d}' if day<22 else '2010-03-01','actual':v} for day,v in zip([1,8,15,22],[4,8,12,16])]+[{'cutoff':'2010-03-01','week_end_exclusive':'2010-03-08','actual':20}]


def test_forecasts_use_only_previous_weeks():
    rows=weekly()
    result=forecasts(rows,'2010-03-01','2010-03-08',['previous_week','mean_previous_4_weeks'])
    assert [(r['method'],r['prediction']) for r in result]==[('previous_week',16.0),('mean_previous_4_weeks',10.0)]
    rows[-1]['actual']=999
    assert [r['prediction'] for r in forecasts(rows,'2010-03-01','2010-03-08',['previous_week','mean_previous_4_weeks'])]==[16.0,10.0]


def test_forecasts_reject_duplicate_or_missing_week():
    rows=weekly()
    with pytest.raises(ValueError):forecasts([*rows,rows[-1]],'2010-03-01','2010-03-08',['previous_week'])
    with pytest.raises(ValueError):forecasts(rows[1:3]+rows[4:],'2010-03-01','2010-03-08',['previous_week'])


def test_metrics_and_tie_keep_baseline():
    assert metrics([{'actual':10,'prediction':8},{'actual':20,'prediction':24}])=={'weeks':2,'actual_total':30,'WAPE':0.2,'MAE':3.0,'bias':1.0}
    assert choose_method({'previous_week':{'WAPE':0.2},'mean_previous_4_weeks':{'WAPE':0.2}})=='previous_week'
    assert choose_method({'previous_week':{'WAPE':0.3},'mean_previous_4_weeks':{'WAPE':0.2}})=='mean_previous_4_weeks'


def test_zero_metric_denominator_is_rejected():
    with pytest.raises(ValueError):metrics([{'actual':0,'prediction':1}])


def test_runner_persists_reloads_and_evaluates_only_selected_final_method(tmp_path):
    import csv,gzip,json,hashlib
    from datetime import date,timedelta
    from run_forecast import run_pipeline
    project=tmp_path/'project'
    (project/'data/raw').mkdir(parents=True)
    (project/'analysis').mkdir()
    import shutil
    for name in ('forecast.py','run_forecast.py'):
        shutil.copyfile(Path(__file__).resolve().parents[1]/name,project/'analysis'/name)
    source=project/'data/raw/transactions_normalized.csv.gz'
    records=[row(str(i),(date(2010,1,5)+timedelta(weeks=i)).isoformat()+' 09:00:00') for i in range(10)]
    with gzip.open(source,'wt',newline='') as stream:
        writer=csv.DictWriter(stream,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    protocol={'source_expected_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'development_start':'2010-02-08','development_end_exclusive':'2010-02-22','final_start':'2010-02-22','final_end_exclusive':'2010-03-08'}
    (project/'analysis/protocol.json').write_text(json.dumps(protocol))
    result=run_pipeline(project,tmp_path/'outputs')
    assert result['selected_method']=='previous_week'
    assert result['final']['WAPE']==0.0 and result['final']['weeks']==2
    with (tmp_path/'outputs/final_predictions.csv').open() as stream:
        assert {r['method'] for r in csv.DictReader(stream)}=={'previous_week'}
    assert (tmp_path/'outputs/weekly_counts.csv').is_file()
    assert (tmp_path/'outputs/strategy.json').is_file()
    with pytest.raises(FileExistsError):run_pipeline(project,tmp_path/'outputs')
