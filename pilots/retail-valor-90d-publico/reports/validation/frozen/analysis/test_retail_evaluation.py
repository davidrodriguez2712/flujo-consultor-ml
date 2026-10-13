import copy
import pandas as pd
import pytest
from retail_evaluation import top_k,ranking_metrics,select_development,acceptance_decision

def predictions():return pd.DataFrame({'customer_id':['2','10','1'],'cutoff':[pd.Timestamp('2011-09-01')]*3,'score':[5.,5.,9.]})
def outcomes():
 f=predictions()[['customer_id','cutoff']].copy();f['target_sales_90d']=[20.,10.,30.];f['horizon_complete']=True;return f
C={'development_acceptance':{'minimum_periods':2},'models_fixed':[{'id':'ridge_log'},{'id':'hist_gradient_log'}]}
def dev(values):return {'periods':[{'cutoff':str(i),'metrics':{k:{'top_k_sales':v} for k,v in zip(['historical_sales','ridge_log','hist_gradient_log'],row)}} for i,row in enumerate(values)]}

def test_k_small_population_and_lexical_ties():
 assert top_k(predictions(),100).customer_id.tolist()==['1','10','2']
 assert top_k(predictions(),2).customer_id.tolist()==['1','10']

@pytest.mark.parametrize('issue',['duplicate','missing','incomplete','negative','nan'])
def test_invalid_outcomes_rejected(issue):
 f=outcomes()
 if issue=='duplicate':f=pd.concat([f,f.iloc[:1]],ignore_index=True)
 elif issue=='missing':f=f.iloc[:2]
 elif issue=='incomplete':f.loc[0,'horizon_complete']=False
 elif issue=='negative':f.loc[0,'target_sales_90d']=-1
 else:f.loc[0,'target_sales_90d']=float('nan')
 with pytest.raises(ValueError):ranking_metrics(predictions(),f,100)

def test_zero_sales_no_invented_share():
 f=outcomes();f['target_sales_90d']=0
 m=ranking_metrics(predictions(),f,100);assert m['sales_share'] is None;assert m['top1_sales_share_within_top_k'] is None
 assert m['effective_k']==3;assert m['top_k_sales']==0

def test_metrics_hand_calculation():
 m=ranking_metrics(predictions(),outcomes(),2)
 assert m['top_k_sales']==40;assert m['sales_share']==pytest.approx(2/3)
 assert m['mae']==pytest.approx((15+5+21)/3)
 assert m['top1_sales_share_within_top_k']==.75

def test_duplicate_predictions_or_nonfinite_scores_rejected():
 with pytest.raises(ValueError):top_k(pd.concat([predictions(),predictions().iloc[:1]]),100)
 f=predictions();f.loc[0,'score']=float('inf')
 with pytest.raises(ValueError):top_k(f,100)

def test_aggregate_gain_but_majority_losses_not_eligible():
 d=dev([(100,90,80),(100,90,80),(100,90,80),(100,200,80)])
 assert select_development(d,C)['selected_method']=='historical_sales'

def test_ties_keep_baseline_and_simple_preferred_if_complex_not_always_better():
 assert select_development(dev([(100,100,100),(100,100,100)]),C)['selected_method']=='historical_sales'
 d=dev([(100,120,130),(100,140,135)])
 assert select_development(d,C)['selected_method']=='ridge_log'
 assert select_development(dev([(100,120,130),(100,120,130)]),C)['selected_method']=='hist_gradient_log'

def test_holdout_cannot_select_another_model_and_tie_keeps_baseline():
 d=dev([(100,120,90),(100,120,90)])
 h={'historical_sales':{'top_k_sales':100},'ridge_log':{'top_k_sales':90},'hist_gradient_log':{'top_k_sales':999}}
 assert acceptance_decision(d,h,C)['recommended_method']=='historical_sales'
 h['ridge_log']['top_k_sales']=100;assert acceptance_decision(d,h,C)['recommended_method']=='historical_sales'
 h['ridge_log']['top_k_sales']=101;assert acceptance_decision(d,h,C)['recommended_method']=='ridge_log'

def test_insufficient_development_or_missing_selected_outcome_rejected():
 with pytest.raises(ValueError):select_development(dev([(100,120,90)]),C)
 with pytest.raises(ValueError):acceptance_decision(dev([(100,120,90),(100,120,90)]),{'historical_sales':{'top_k_sales':100}},C)
