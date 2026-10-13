"""Reproduce estrategia congelada en copia aislada; no redefine holdout ni approvals."""
import argparse
from datetime import datetime,timezone
import importlib.metadata
import json
from pathlib import Path
import platform
import time
import numpy as np
import pandas as pd
from retail_source import load_transactions,FIELDS
from retail_temporal import reconcile_transactions,valid_purchases,build_snapshot,training_rows,FEATURES
from retail_models import fit_predict,MODEL_IDS
from retail_evaluation import ranking_metrics,top_k,select_development,acceptance_decision
from run_retail import checked_contracts,read_snapshots,sha256

RTOL=1e-8
ATOL=1e-6

def output_directory(root,out):
    root=root.resolve();out=out.resolve()
    if out==root or not out.is_relative_to(root):raise ValueError('output debe ser subcarpeta nueva dentro de la copia aislada')
    if out.exists():raise ValueError('output existente: no sobrescribir reproducción')
    out.mkdir(parents=True)
    return out

def compare_frames(actual,expected,keys,numeric):
    assert set(actual.columns)==set(expected.columns),'columnas diferentes'
    assert not actual.duplicated(keys).any() and not expected.duplicated(keys).any(),'keys repetidas'
    a=actual.sort_values(keys,kind='stable').reset_index(drop=True)[expected.columns]
    b=expected.sort_values(keys,kind='stable').reset_index(drop=True)
    assert len(a)==len(b),'número de filas diferente'
    other=[k for k in b.columns if k not in numeric]
    pd.testing.assert_frame_equal(a[other],b[other],check_dtype=False,check_exact=True)
    if numeric:np.testing.assert_allclose(a[numeric].to_numpy(dtype=float),b[numeric].to_numpy(dtype=float),rtol=RTOL,atol=ATOL,equal_nan=True)
    return {'rows':len(a),'keys':'EXACT','non_numeric':'EXACT','numeric_rtol':RTOL,'numeric_atol':ATOL}

def compare_selections(actual,expected):
    for k in ['selected_method','period_count','reason']:assert actual[k]==expected[k], 'selección no coincide'
    assert set(actual['candidate_checks'])==set(expected['candidate_checks'])
    for method,check in actual['candidate_checks'].items():
        previous=expected['candidate_checks'][method]
        for k in ['eligible','losing_periods']:assert check[k]==previous[k]
        for k in ['aggregate_sales','baseline_aggregate_sales']:np.testing.assert_allclose(check[k],previous[k],rtol=RTOL,atol=ATOL)


def persist_and_read_snapshots(frame,path):
    frame.to_csv(path,index=False)
    return read_snapshots(path)

def reproduce(root,out):
    start=time.monotonic();root=root.resolve();b=checked_contracts(root)
    verified={}
    for rel in ['reports/discovery/evidence-manifest-02.json','reports/framing/evidence-manifest.json','reports/diagnosis/evidence-manifest.json','reports/execution/evidence-manifest.json','reports/execution/dataset-manifest.json','reports/validation/evidence-manifest.json','reports/delivery/evidence-manifest.json']:
        m=json.loads((root/rel).read_text())
        for name,r in m['files'].items():
            path=(root/name).resolve()
            if not path.is_relative_to(root):raise ValueError('manifest escapa de copia')
            if sha256(path)!=r['sha256']:raise ValueError('evidencia de referencia modificada: '+name)
        verified[rel]=len(m['files'])
    source=root/'data/raw/online_retail_II.xlsx'
    if sha256(source)!=json.loads((root/'data/source_manifest.json').read_text())['sha256']:raise ValueError('fuente raw cambió')
    out=output_directory(root,out)
    f,metadata=load_transactions(source)
    reference=pd.read_csv(root/'data/interim/transactions_normalized.csv.gz',dtype={k:'string' for k in ['invoice_id','stock_code','description','customer_id','country','source_sheet']},parse_dates=['invoice_at'])
    comparisons={'normalization':compare_frames(f,reference,['source_sheet','source_row'],['quantity','unit_price','source_row'])}
    del reference
    # El flujo original persiste normalizado y vuelve a leer CSV antes de agregar.
    f.to_csv(out/'transactions_normalized.csv.gz',index=False)
    f=pd.read_csv(out/'transactions_normalized.csv.gz',dtype={k:'string' for k in ['invoice_id','stock_code','description','customer_id','country','source_sheet']},parse_dates=['invoice_at'])
    r=reconcile_transactions(f,b['retail']);r.attrs={}
    v=valid_purchases(r,b['retail']);v.attrs={};del r
    e=b['evaluation'];allcut=sorted(set(x['cutoff'] for x in e['cutoffs'])|{t for x in e['cutoffs'] for t in x['mature_training_cutoffs']})
    finalitem=next(x for x in e['cutoffs'] if x['purpose']=='holdout');final_t=pd.Timestamp(finalitem['cutoff'])
    snapshots=[];final=None
    for value in allcut:
        t=pd.Timestamp(value);s=build_snapshot(v,t,b['retail'],f.invoice_at.max(),observed_from=f.invoice_at.min())
        if t==final_t:final=s
        else:snapshots.append(s)
    rows=pd.concat(snapshots,ignore_index=True)
    comparisons['snapshots']=compare_frames(rows,read_snapshots(root/'data/processed/customer_snapshots.csv'),['customer_id','cutoff'],FEATURES+['target_sales_90d'])
    comparisons['reserved_final_snapshot']=compare_frames(final,read_snapshots(root/'data/processed/reserved/holdout_snapshot.csv'),['customer_id','cutoff'],FEATURES+['target_sales_90d'])
    # Respetar también el límite de persistencia de snapshots usado al entrenar.
    rows=persist_and_read_snapshots(rows,out/'customer_snapshots.csv');final=persist_and_read_snapshots(final,out/'holdout_snapshot.csv')
    predictions=[];periods=[]
    for item in e['cutoffs']:
        if item['purpose']!='development':continue
        t=pd.Timestamp(item['cutoff']);train=training_rows(rows,t);score=rows.loc[rows.cutoff==t].copy();metrics={}
        outcomes=score[['customer_id','cutoff','target_sales_90d']].copy();outcomes['horizon_complete']=True
        for method in MODEL_IDS:
            pred=fit_predict(train,score.drop(columns='target_sales_90d'),method,20261009)
            metric=ranking_metrics(pred,outcomes,b['retail']['capacity'])
            if method=='rfm':metric['mae']=None;metric['mae_note']='Score ordinal; no error monetario.'
            metrics[method]=metric;pred['model_id']=method;predictions.append(pred)
        periods.append({'cutoff':t.isoformat(),'metrics':metrics})
    devpred=pd.concat(predictions,ignore_index=True)
    expected=pd.read_csv(root/'data/processed/development_predictions.csv',dtype={'customer_id':'string'},parse_dates=['cutoff'])
    comparisons['development_predictions']=compare_frames(devpred,expected,['model_id','customer_id','cutoff'],['score'])
    devpred.to_csv(out/'development_predictions.csv',index=False)
    development={'periods':periods};selection=select_development(development,e)
    frozen=json.loads((root/'reports/validation/development-selection.json').read_text())
    compare_selections(selection,frozen['selection'])
    for a,previous in zip(periods,frozen['development']['periods']):
        assert a['cutoff']==previous['cutoff']
        for method in MODEL_IDS:
            for key,value in a['metrics'][method].items():
                expected=previous['metrics'][method][key]
                if value is None or isinstance(value,str):assert value==expected
                else:np.testing.assert_allclose(value,expected,rtol=RTOL,atol=ATOL)
    train=training_rows(rows,final_t);method=selection['selected_method']
    methods=['historical_sales']+([method] if method!='historical_sales' else [])
    finaloutcomes=final[['customer_id','cutoff','target_sales_90d']].copy();finaloutcomes['horizon_complete']=True
    finalpreds=[];metrics={}
    for method in methods:
        pred=fit_predict(train,final.drop(columns='target_sales_90d'),method,20261009);metrics[method]=ranking_metrics(pred,finaloutcomes,b['retail']['capacity']);pred['model_id']=method;finalpreds.append(pred)
    fp=pd.concat(finalpreds,ignore_index=True)
    expected=pd.read_csv(root/'data/processed/holdout_predictions.csv',dtype={'customer_id':'string'},parse_dates=['cutoff'])
    comparisons['holdout_predictions']=compare_frames(fp,expected,['model_id','customer_id','cutoff'],['score'])
    fp.to_csv(out/'holdout_predictions.csv',index=False)
    decision=acceptance_decision(development,metrics,e);original=json.loads((root/'reports/validation/holdout-results.json').read_text());assert decision['recommended_method']==original['decision']['recommended_method'];assert decision['holdout_rule']==original['decision']['holdout_rule'];assert decision['scope']==original['decision']['scope'];compare_selections(decision['development_selection'],original['decision']['development_selection'])
    for method,values in metrics.items():
        for key,value in values.items():np.testing.assert_allclose(value,original['metrics'][method][key],rtol=RTOL,atol=ATOL)
    ranking=top_k(fp.loc[fp.model_id==decision['recommended_method']],b['retail']['capacity']);ranking.insert(0,'rank',range(1,len(ranking)+1))
    expected=pd.read_csv(root/'delivery/prioritization_retrospective.csv',dtype={'customer_id':'string'},parse_dates=['cutoff'])
    comparisons['selected_ranking']=compare_frames(ranking,expected,['rank'],['score'])
    ranking.to_csv(out/'prioritization_retrospective.csv',index=False)
    report={'status':'PASS','finished_at_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'environment':{'python':platform.python_version(),'platform':platform.platform(),'packages':{name:importlib.metadata.version(name) for name in ['pandas','numpy','openpyxl','scikit-learn','pytest']}},'rtol':RTOL,'atol':ATOL,'comparisons':comparisons,'development_metrics':'MATCH','final_metrics':'MATCH','decision':'EXACT','selected_method':decision['recommended_method'],'historical_manifests_verified':verified,'source_sha256':sha256(source),'original_holdout_marker_unchanged':'CHECK_BY_COORDINATOR','api_cost_usd':0,'interpretation':'Reproducción misma fuente/configuración/resultados en copia; no evaluación nueva ni selección adicional.','foundry_runtime_dependency':False}
    (out/'reproduction.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'status':'PASS','selected_method':decision['recommended_method'],'comparisons':list(comparisons),'api_cost_usd':0}))
    return report

def main(argv=None):
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path('.'));p.add_argument('--out',type=Path);a=p.parse_args(argv);root=a.root.resolve()
    return reproduce(root,a.out.resolve() if a.out else root/'reproduced')

if __name__=='__main__':main()
