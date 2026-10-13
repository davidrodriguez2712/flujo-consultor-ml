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
from retail_evaluation import ranking_metrics,top_k,select_development,acceptance_decision

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

def checked_holdout_selection(root):
    if (root/'reports/validation/holdout-attempt.json').exists():raise ValueError('holdout ya ejecutado/iniciado; sin reintentos automáticos')
    approval=root/'reports/execution/human-approval.json'
    if not approval.is_file():raise ValueError('holdout reservado: falta aprobación Execution')
    a=json.loads(approval.read_text());manifest=root/'reports/execution/evidence-manifest.json'
    if a.get('decision')!='PASS' or a.get('stage')!='execution' or sha256(manifest)!=a.get('execution_manifest_sha256'):raise ValueError('holdout reservado: aprobación Execution inválida')
    for rel,r in json.loads(manifest.read_text())['files'].items():
        if sha256(checked_path(root,rel))!=r['sha256']:raise ValueError('evidencia Execution modificada: '+rel)
    frozen=root/'reports/validation/development-selection.json';m=root/'reports/validation/selection-manifest.json'
    if not frozen.is_file() or not m.is_file():raise ValueError('holdout reservado: selección no congelada')
    if sha256(frozen)!=json.loads(m.read_text())['sha256']:raise ValueError('selección congelada modificada')
    return json.loads(frozen.read_text())

def holdout(root):
    frozen=checked_holdout_selection(root);b=checked_contracts(root)
    for rel,r in json.loads((root/'reports/execution/dataset-manifest.json').read_text())['files'].items():
        if sha256(checked_path(root,rel))!=r['sha256']:raise ValueError('dataset/fuente cambió: '+rel)
    expected=select_development(frozen['development'],b['evaluation'])
    if expected!=frozen['selection'] or expected['selected_method']!=frozen['selected_method']:raise ValueError('selección no coincide con development')
    # development usado por la selección también debe permanecer congelado.
    for rel,h in frozen['input_sha256'].items():
        if sha256(checked_path(root,rel))!=h:raise ValueError('input de selección modificado: '+rel)
    out=root/'data/processed/holdout_predictions.csv'
    if out.exists():raise ValueError('holdout ya tiene outputs; sin sobrescritura')
    attempt=root/'reports/validation/holdout-attempt.json'
    record={'started_at_utc':datetime.now(timezone.utc).isoformat(),'status':'STARTED','selection_sha256':sha256(root/'reports/validation/development-selection.json'),'api_cost_usd':0}
    with attempt.open('x') as stream:json.dump(record,stream,indent=2)
    start=time.monotonic()
    try:
        item=next(x for x in b['evaluation']['cutoffs'] if x['purpose']=='holdout');t=pd.Timestamp(item['cutoff'])
        train=training_rows(read_snapshots(root/'data/processed/customer_snapshots.csv'),t)
        score=read_snapshots(root/'data/processed/reserved/holdout_snapshot.csv')
        if len(score)!=item['eligible_customers'] or not score.cutoff.eq(t).all() or not score.label_end.eq(pd.Timestamp(item['label_end'])).all():raise ValueError('holdout población/ventana difiere de contrato')
        if sorted(v.isoformat() for v in train.cutoff.unique())!=sorted(item['mature_training_cutoffs']):raise ValueError('train final no maduro/calendario cambió')
        selected=frozen['selected_method'];methods=['historical_sales']+([selected] if selected!='historical_sales' else [])
        outcomes=score[['customer_id','cutoff','target_sales_90d']].copy();outcomes['horizon_complete']=True
        predictions=[];metrics={}
        for method in methods:
            pred=fit_predict(train,score.drop(columns='target_sales_90d'),method,20261009)
            metrics[method]=ranking_metrics(pred,outcomes,b['retail']['capacity'])
            pred['model_id']=method;predictions.append(pred)
        decision=acceptance_decision(frozen['development'],metrics,b['evaluation'])
        pd.concat(predictions,ignore_index=True).to_csv(out,index=False)
        recommended=decision['recommended_method'];chosen=next(x for x in predictions if x.model_id.iloc[0]==recommended)
        ranking=top_k(chosen,b['retail']['capacity']);ranking.insert(0,'rank',range(1,len(ranking)+1))
        (root/'delivery').mkdir(exist_ok=True);ranking.to_csv(root/'delivery/prioritization_retrospective.csv',index=False)
        report={'finished_at_utc':datetime.now(timezone.utc).isoformat(),'elapsed_seconds':time.monotonic()-start,'cutoff':t.isoformat(),'label_end':item['label_end'],'train_rows':len(train),'max_train_label_end':train.label_end.max().isoformat(),'evaluated_methods':methods,'metrics':metrics,'decision':decision,'selection_sha256':record['selection_sha256'],'api_cost_usd':0,'interpretation':'Si seleccionado es baseline, final es descriptivo; no comparación con modelos descartados ni afirmación de mejora.'}
        (root/'reports/validation/holdout-results.json').write_text(json.dumps(report,indent=2)+'\n')
        record.update(status='COMPLETED',finished_at_utc=report['finished_at_utc'],result_sha256=sha256(root/'reports/validation/holdout-results.json'))
        attempt.write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps({'holdout':'COMPLETED','evaluated_methods':methods,'recommended_method':recommended,'api_cost_usd':0}))
        return report
    except Exception as exc:
        record.update(status='FAILED',error_type=type(exc).__name__,error=str(exc));attempt.write_text(json.dumps(record,indent=2)+'\n');raise


def main(argv=None):
    parser=argparse.ArgumentParser();parser.add_argument('command',choices=['development','holdout']);parser.add_argument('--root',type=Path,default=Path('.'));a=parser.parse_args(argv)
    if a.command=='holdout':return holdout(a.root.resolve())
    return development(a.root.resolve())

if __name__=='__main__':main()
