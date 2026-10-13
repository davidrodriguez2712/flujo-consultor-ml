import pandas as pd
import pytest
from reproduce_retail import compare_frames,output_directory

def frame():return pd.DataFrame({'id':['2','1'],'score':[3.,7.],'method':['baseline','baseline']})

def test_order_independent_exact_keys_with_numeric_tolerance():
 a=frame();b=a.iloc[::-1].copy();b['score']+=1e-7
 result=compare_frames(a,b,['id'],['score']);assert result['rows']==2

def test_keys_duplicate_or_changed_and_method_change_fail():
 a=frame()
 for b in [pd.concat([a,a.iloc[:1]]),a.assign(id=['3','1']),a.assign(method='other')]:
  with pytest.raises(AssertionError):compare_frames(a,b,['id'],['score'])

def test_excess_numeric_drift_fails():
 a=frame();b=a.copy();b.loc[0,'score']+=.01
 with pytest.raises(AssertionError):compare_frames(a,b,['id'],['score'])

def test_reproduction_output_must_be_new_and_in_copy(tmp_path):
 with pytest.raises(ValueError):output_directory(tmp_path,tmp_path.parent/'external')
 with pytest.raises(ValueError):output_directory(tmp_path,tmp_path)
 out=output_directory(tmp_path,tmp_path/'reproduced');assert out.is_dir()
 with pytest.raises(ValueError):output_directory(tmp_path,out)

def test_selection_identity_exact_but_metrics_follow_tolerance():
 from reproduce_retail import compare_selections
 a={'selected_method':'historical_sales','period_count':4,'reason':'same','candidate_checks':{'ridge_log':{'eligible':False,'losing_periods':4,'aggregate_sales':100.,'baseline_aggregate_sales':110.}}}
 import copy
 b=copy.deepcopy(a);b['candidate_checks']['ridge_log']['aggregate_sales']+=1e-7
 compare_selections(a,b)
 b['selected_method']='ridge_log'
 with pytest.raises(AssertionError):compare_selections(a,b)

def test_reproduction_uses_persisted_snapshots_as_original_runner(tmp_path):
 from reproduce_retail import persist_and_read_snapshots
 from retail_temporal import FEATURES
 f=pd.DataFrame({k:[.30000000000000004] for k in FEATURES})
 f['customer_id']='1'
 for col in ['cutoff','label_end','history_min_at','history_max_at','target_min_at','target_max_at']:f[col]=pd.Timestamp('2011-01-01')
 f['target_sales_90d']=.30000000000000004
 path=tmp_path/'snapshot.csv'
 out=persist_and_read_snapshots(f,path)
 from run_retail import read_snapshots
 pd.testing.assert_frame_equal(out,read_snapshots(path))
 assert out.sales_90d.iloc[0]==.3
 assert f.sales_90d.iloc[0]!=out.sales_90d.iloc[0]
