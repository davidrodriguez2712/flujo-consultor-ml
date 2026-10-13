import numpy as np
import pandas as pd
import pytest
from retail_models import fit_predict
from retail_temporal import FEATURES

def rows(n=30,cutoff='2010-06-01'):
 f=pd.DataFrame({k:np.arange(n,dtype=float)+1 for k in FEATURES})
 f['customer_id']=[str(i) for i in range(n)];f['cutoff']=pd.Timestamp(cutoff)
 f['label_end']=f.cutoff+pd.Timedelta(days=90);f['target_sales_90d']=np.arange(n,dtype=float)*7
 return f

@pytest.mark.parametrize('model',['historical_sales','rfm','ridge_log','hist_gradient_log'])
def test_scoring_target_not_input_and_ids_preserve_alignment(model):
 train=rows();score=rows(6,'2010-09-01');a=fit_predict(train,score,model,20261009)
 changed=score.copy();changed['target_sales_90d']=999999
 b=fit_predict(train,changed.sample(frac=1,random_state=3),model,20261009)
 aa=a.sort_values('customer_id');bb=b.sort_values('customer_id')
 assert aa.customer_id.tolist()==bb.customer_id.tolist()
 np.testing.assert_allclose(aa.score,bb.score,rtol=1e-12,atol=1e-12)
 assert a.columns.tolist()==['customer_id','cutoff','score']

@pytest.mark.parametrize('model',['historical_sales','rfm','ridge_log','hist_gradient_log'])
def test_empty_train_and_nonfinite_rejected(model):
 train=rows();score=rows(6,'2010-09-01')
 with pytest.raises(ValueError,match='vacío'):fit_predict(train.iloc[:0],score,model,1)
 score.loc[0,'sales_90d']=np.inf
 with pytest.raises(ValueError,match='finitas'):fit_predict(train,score,model,1)

def test_unknown_model_and_unmature_training_rejected():
 with pytest.raises(ValueError,match='modelo'):fit_predict(rows(),rows(6,'2010-09-01'),'other',1)
 with pytest.raises(ValueError,match='madur'):fit_predict(rows(cutoff='2010-08-01'),rows(6,'2010-09-01'),'ridge_log',1)

def test_baseline_exact_and_rfm_direction():
 tr=rows();sc=rows(3,'2010-09-01')
 assert fit_predict(tr,sc,'historical_sales',1).score.tolist()==sc.sales_90d.tolist()
 sc['recency_days']=[3,2,1]
 assert fit_predict(tr,sc,'rfm',1).score.tolist()==pytest.approx([1/3,2/3,1])

def test_invalid_target_or_duplicate_scoring_key_rejected():
 tr=rows();sc=rows(3,'2010-09-01');tr.loc[0,'target_sales_90d']=-1
 with pytest.raises(ValueError,match='target'):fit_predict(tr,sc,'ridge_log',1)
 sc.loc[1,'customer_id']=sc.loc[0,'customer_id']
 with pytest.raises(ValueError,match='key'):fit_predict(rows(),sc,'ridge_log',1)
