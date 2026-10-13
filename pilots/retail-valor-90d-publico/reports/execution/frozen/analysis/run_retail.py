"""Runner local del benchmark; development separado del holdout reservado."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
from pathlib import Path
import time
import numpy as np
import pandas as pd
from retail_models import fit_predict,MODEL_IDS
from retail_temporal import training_rows,FEATURES

def sha256(path):
    digest=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):digest.update(block)
    return digest.hexdigest()

def checked_path(root,rel):
    path=(root/rel).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('path fuera del proyecto')
    return path

def checked_contracts(root):
    compiled=root/'reports/execution/approved-contracts.json'
    b=json.loads(compiled.read_text())
    a=json.loads((root/'reports/diagnosis/human-approval.json').read_text())
    if sha256(compiled)!=a.get('compiled_contract_sha256'):raise ValueError('representación del contrato modificada')
    if a['decision']!='PASS' or a['contracts']!=b['approved_sha256']:raise ValueError('contratos no aprobados')
    for rel,h in b['approved_sha256'].items():
        if sha256(checked_path(root,rel))!=h:raise ValueError('hash de contrato cambió: '+rel)
    # La representación JSON debe coincidir con la copia aprobada original.
    # Su hash se fija en el manifiesto de execution y se verifica antes de evaluar.
    return b

def read_snapshots(path):
    return pd.read_csv(path,dtype={'customer_id':'string'},parse_dates=['cutoff','label_end','history_min_at','history_max_at','target_min_at','target_max_at'])

def development(root):
    start=time.monotonic();b=checked_contracts(root);evaluation=b['evaluation']
    m=json.loads((root/'reports/execution/dataset-manifest.json').read_text())
    for rel,record in m['files'].items():
        if sha256(checked_path(root,rel))!=record['sha256']:raise ValueError('hash dataset/fuente cambió: '+rel)
    rows=read_snapshots(root/'data/processed/customer_snapshots.csv')
    holdout=next(pd.Timestamp(x['cutoff']) for x in evaluation['cutoffs'] if x['purpose']=='holdout')
    if (rows.cutoff>=holdout).any():raise ValueError('holdout mezclado en development')
    predictions=[];runs=[];metrics=[]
    for item in evaluation['cutoffs']:
        if item['purpose']!='development':continue
        t=pd.Timestamp(item['cutoff']);train=training_rows(rows,t);score=rows.loc[rows.cutoff==t].copy()
        if len(score)!=item['eligible_customers']:raise ValueError('población difiere del contrato')
        expected=sorted(item['mature_training_cutoffs'])
        if sorted(v.isoformat() for v in train.cutoff.unique())!=expected:raise ValueError('calendario train cambió')
        for model_id in MODEL_IDS:
            before=time.monotonic();pred=fit_predict(train,score,model_id,20261009);pred['model_id']=model_id
            predictions.append(pred);runs.append({'cutoff':t.isoformat(),'model_id':model_id,'train_rows':len(train),'score_rows':len(pred),'seconds':time.monotonic()-before,'feature_columns':FEATURES,'max_train_label_end':train.label_end.max().isoformat()})
            joined=pred.merge(score[['customer_id','cutoff','target_sales_90d']],on=['customer_id','cutoff'],validate='one_to_one')
            ranked=joined.sort_values(['score','customer_id'],ascending=[False,True],kind='stable')
            k=min(b['retail']['capacity'],len(joined));total=float(joined.target_sales_90d.sum());top=float(ranked.head(k).target_sales_90d.sum())
            metrics.append({'cutoff':t.isoformat(),'model_id':model_id,'effective_k':k,'eligible_count':len(joined),'top_k_sales':top,'sales_share':top/total if total>0 else None,'mae':float(np.mean(np.abs(joined.score-joined.target_sales_90d))) if model_id!='rfm' else None,'mae_note':'RFM score es ordinal; MAE monetario no aplicable.' if model_id=='rfm' else None})
    out=root/'data/processed/development_predictions.csv'
    if out.exists():raise ValueError('outputs existentes: no sobrescribir development congelado')
    pd.concat(predictions,ignore_index=True).to_csv(out,index=False)
    report={'created_at_utc':datetime.now(timezone.utc).isoformat(),'api_cost_usd':0,'elapsed_seconds':time.monotonic()-start,'seed':20261009,'models':evaluation['models_fixed'],'baseline':'historical_sales','rfm_role':'Comparador ordinal informativo; sin selección.','runs':runs,'metrics':metrics,'holdout_outcomes_inspected':False,'selection_status':'Pendiente decisión development congelada en Validation; no holdout ejecutado.'}
    (root/'reports/execution/model_runs.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'runs':len(runs),'prediction_rows':sum(r['score_rows'] for r in runs),'holdout':'reservado','api_cost_usd':0}))
    return report

def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['development','holdout']);parser.add_argument('--root',type=Path,default=Path('.'));a=parser.parse_args(argv)
    if a.command=='holdout':raise ValueError('holdout reservado hasta aprobación Execution y selección congelada')
    return development(a.root.resolve())

if __name__=='__main__':main()
