"""Regresiones del baseline analítico del piloto; no cambian tests de ACOS."""
import pytest
from baseline import fit,predict,evaluate


def row(cid='A',label=0,available='2024-03-08T00:00:00Z',**changes):
    result={'customer_id':cid,'prediction_timestamp':'2024-02-01T00:00:00Z',
        'label_available_at':available,'target':label,'active_days_prev_month':'10',
        'active_days_prev2_month':'20','failed_payments_prev_month':'0',
        'support_tickets_prev_month':'0','mrr_usd':'29'}
    result.update(changes)
    return result


def test_future_label_cannot_enter_training():
    with pytest.raises(ValueError,match='disponible'):
        fit([row(available='2024-04-08T00:00:00Z')],'2024-04-01T00:00:00Z')


def test_pending_label_cannot_enter_training():
    with pytest.raises(ValueError,match='binary'):
        fit([row(label=None)],'2024-04-01T00:00:00Z')


def test_training_row_after_training_cutoff_rejected():
    with pytest.raises(ValueError,match='scoring'):
        fit([row(prediction_timestamp='2024-05-01T00:00:00Z')],'2024-04-01T00:00:00Z')


def test_outcomes_and_identifier_do_not_change_score():
    model=fit([row(),row('B',1)],'2024-04-01T00:00:00Z')
    original=predict(model,[row()])[0]['score']
    dangerous=row('ZZZ',1,cancellation_at='2099-01-01',label_status='observed')
    assert predict(model,[dangerous])[0]['score']==original


def test_imputation_learned_on_train_and_not_modified_on_predict():
    model=fit([row(active_days_prev_month='4'),row('B',1,active_days_prev_month='8')],'2024-04-01T00:00:00Z')
    assert model['activity_median']==6
    predict(model,[row(active_days_prev_month='999')])
    assert model['activity_median']==6


def test_exact_top_k_metrics_and_deterministic_tie():
    scores=[{'customer_id':'B','score':0.9},{'customer_id':'A','score':0.9},{'customer_id':'C','score':0.1}]
    actual=[row('B',0),row('A',1),row('C',1)]
    result=evaluate(scores,actual,2)
    assert result['selected_ids']==['A','B']
    assert result['precision']==0.5 and result['recall']==0.5
    assert result['prevalence']==pytest.approx(2/3)
    assert result['lift']==pytest.approx(0.75)


def test_no_positive_recall_and_lift_undefined_and_capacity_capped():
    scores=[{'customer_id':'A','score':0.1}]
    result=evaluate(scores,[row()],50)
    assert result['k_effective']==1 and result['recall'] is None and result['lift'] is None


def test_prediction_without_target_does_not_require_label():
    model=fit([row(),row('B',1)],'2024-04-01T00:00:00Z')
    sample=row();sample.pop('target');sample.pop('label_available_at')
    assert len(predict(model,[sample]))==1
