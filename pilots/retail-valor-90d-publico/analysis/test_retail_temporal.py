import copy
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal
from retail_temporal import valid_purchases, reconcile_transactions, build_snapshot, training_rows

C={'history_days':180,'baseline_days':90,'horizon_days':90,'purchase_validity':{'stock_code_regex':r'^\d{5}[A-Za-z]*$'},'reconciliation':{'fields':['invoice_id','stock_code','description','quantity','invoice_at','unit_price','customer_id','country']}}
T=pd.Timestamp('2011-01-01')
def frame(rows):
 f=pd.DataFrame(rows,columns=['invoice_at','quantity','unit_price','customer_id','invoice_id','stock_code'])
 f['invoice_at']=pd.to_datetime(f.invoice_at);f['description']='goods';f['country']='UK';f['source_sheet']='A';f['source_row']=range(2,len(f)+2)
 return f

def example():return frame([['2010-12-01',2,3,'1','I1','12345'],['2011-01-01',4,5,'1','I2','12345'],['2011-04-01',9,10,'1','I3','12345']])

def build(f):return build_snapshot(f,T,C,pd.Timestamp('2011-04-01'),observed_from=pd.Timestamp('2010-01-01'))

def test_half_open_boundaries_and_no_input_mutation():
 f=example();before=f.copy(deep=True);s=build(f)
 assert s.loc[0,'sales_180d']==6
 assert s.loc[0,'target_sales_90d']==20
 assert s.loc[0,'orders_180d']==1
 assert s.loc[0,'history_max_at']<T
 assert_frame_equal(f,before)

def test_full_horizon_and_history_required():
 with pytest.raises(ValueError,match='horizonte'):build_snapshot(example(),T,C,T+pd.Timedelta(days=89),observed_from=pd.Timestamp('2010-01-01'))
 with pytest.raises(ValueError,match='historia'):build_snapshot(example(),T,C,T+pd.Timedelta(days=90),observed_from=T-pd.Timedelta(days=179))

def test_zero_future_is_zero_and_future_does_not_affect_features():
 f=example();s=build(f);g=f.copy();g.loc[g.invoice_at>=T,'quantity']=999
 z=build(g)
 features=['recency_days','orders_90d','orders_180d','sales_90d','sales_180d','units_180d','distinct_products_180d','tenure_observed_days']
 assert_frame_equal(s[features],z[features]);assert build(f.loc[f.invoice_at<T]).target_sales_90d.tolist()==[0]

def test_mature_labels_only_and_scoring_cutoff_not_in_train():
 s=pd.DataFrame({'cutoff':pd.to_datetime(['2010-06-01','2010-07-01']),'label_end':pd.to_datetime(['2010-08-30','2010-09-29'])})
 assert training_rows(s,pd.Timestamp('2010-09-01')).cutoff.tolist()==[pd.Timestamp('2010-06-01')]
 assert len(training_rows(s,pd.Timestamp('2010-08-30')))==1

@pytest.mark.parametrize('field,value,reason',[('invoice_id','c1','cancellation'),('quantity',-1,'nonpositive'),('unit_price',0,'nonpositive'),('customer_id',None,'missing_customer_id'),('stock_code','POST','nonstandard_code')])
def test_exclusions_with_provenance(field,value,reason):
 f=example().iloc[:1].copy();f.loc[f.index[0],field]=value;before=f.copy(deep=True)
 v=valid_purchases(f,C);assert v.empty
 assert v.attrs['excluded'].iloc[0]['exclusion_reason']==reason
 assert v.attrs['excluded'].iloc[0]['source_row']==2
 assert_frame_equal(f,before)

def test_reconcile_max_multiplicity_and_preserve_internal_repetition():
 f=example().iloc[:1];a=pd.concat([f,f],ignore_index=True);a['source_row']=[2,3]
 b=f.copy();b['source_sheet']='B';b['source_row']=2
 original=pd.concat([a,b],ignore_index=True);before=original.copy(deep=True)
 r=reconcile_transactions(original,C);assert len(r)==2
 assert len(r.attrs['copy_map'])==1
 assert len(valid_purchases(r,C))==2
 assert build(r).sales_180d.tolist()==[12]
 assert_frame_equal(original,before)

def test_invoice_frequency_not_line_frequency_and_tenure_uses_past():
 f=frame([['2010-01-01',1,2,'1','OLD','12345'],['2010-12-01',1,2,'1','I','12345'],['2010-12-01',1,3,'1','I','12346']])
 s=build(f);assert s.orders_180d.tolist()==[1];assert s.distinct_products_180d.tolist()==[2]
 assert s.tenure_observed_days.tolist()==[365]
