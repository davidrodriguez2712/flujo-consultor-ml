"""Baseline del piloto: riesgo por grupos, stdlib, sin acceso a métricas de holdout.

Uso: python analysis/baseline.py --output analysis/outputs/baseline-development
"""
import argparse
import csv
import hashlib
import json
import statistics
from collections import defaultdict
from pathlib import Path

POLICY={'version':'1','k':50,'prior_strength':20,'activity_drop_fraction':0.5,
    'features':['active_days_prev_month','active_days_prev2_month','failed_payments_prev_month','support_tickets_prev_month'],
    'development_months':[f'2024-{m:02d}' for m in range(9,13)]+[f'2025-{m:02d}' for m in range(1,6)],
    'final_training_timestamp':'2025-07-01T00:00:00Z','final_model':'fixed; no refit on test',
    'holdout_months':[f'2025-{m:02d}' for m in range(7,13)],'hyperparameter_search':False}


def number(value):
    return None if value in ('',None) else float(value)


def bucket(row,median):
    activity=number(row['active_days_prev_month']);missing=activity is None
    activity=median if missing else activity
    previous=number(row['active_days_prev2_month'])
    if previous is None:raise ValueError('Falta actividad previa')
    drop=previous>0 and activity<=POLICY['activity_drop_fraction']*previous
    return '|'.join(str(int(x)) for x in [missing,drop,
        number(row['failed_payments_prev_month'])>0,number(row['support_tickets_prev_month'])>0])


def fit(rows,training_timestamp):
    if not rows:raise ValueError('Train vacío')
    for row in rows:
        if type(row['target']) is not int or row['target'] not in (0,1):raise ValueError('Target debe ser binary observado')
        if row['prediction_timestamp']>=training_timestamp:raise ValueError('Fila de scoring no anterior al entrenamiento')
        if row['label_available_at']>training_timestamp:raise ValueError('Label no disponible al entrenar')
    observed=[number(r['active_days_prev_month']) for r in rows if number(r['active_days_prev_month']) is not None]
    median=statistics.median(observed) if observed else 0.0
    prevalence=sum(r['target'] for r in rows)/len(rows)
    groups=defaultdict(lambda:[0,0])
    for row in rows:
        counts=groups[bucket(row,median)];counts[0]+=1;counts[1]+=row['target']
    return {'policy_version':POLICY['version'],'training_timestamp':training_timestamp,
        'training_rows':len(rows),'training_positives':sum(r['target'] for r in rows),
        'prevalence':prevalence,'activity_median':median,'all_activity_missing':not observed,
        'prior_strength':POLICY['prior_strength'],'groups':dict(sorted(groups.items()))}


def predict(model,rows):
    scores=[]
    for row in rows:
        count,positives=model['groups'].get(bucket(row,model['activity_median']),(0,0))
        strength=model['prior_strength']
        score=(positives+strength*model['prevalence'])/(count+strength)
        scores.append({'customer_id':row['customer_id'],'score':score})
    return scores


def evaluate(scores,rows,k):
    if not rows or k<=0:raise ValueError('Evaluación vacía o K inválido')
    lookup={r['customer_id']:r for r in rows}
    if len(lookup)!=len(rows):raise ValueError('IDs duplicados en evaluación mensual')
    if len(scores)!=len(rows) or {s['customer_id'] for s in scores}!=set(lookup):raise ValueError('Scores no coinciden con evaluación')
    if any(type(r['target']) is not int or r['target'] not in (0,1) for r in rows):raise ValueError('Target debe ser binary observado')
    selected=sorted(scores,key=lambda r:(-r['score'],r['customer_id']))[:min(k,len(rows))]
    selected_ids=[s['customer_id'] for s in selected]
    positives=sum(r['target'] for r in rows);hits=sum(lookup[c]['target'] for c in selected_ids)
    prevalence=positives/len(rows);precision=hits/len(selected)
    return {'rows':len(rows),'positives':positives,'k_effective':len(selected),'hits':hits,
        'precision':precision,'recall':hits/positives if positives else None,
        'prevalence':prevalence,'lift':precision/prevalence if prevalence else None,
        'random_expected_precision':prevalence,'random_expected_recall':len(selected)/len(rows) if positives else None,
        'selected_ids':selected_ids,
        'selected_positive_mrr':sum(float(lookup[c]['mrr_usd']) for c in selected_ids if lookup[c]['target'])}


def load_development(root):
    # Filtrar fecha ANTES de interpretar target: no utilizar labels individuales del test.
    raw=root/'data/raw';limit='2025-05-01T00:00:00Z'
    targets={}
    with (raw/'churn_labels.csv').open(encoding='utf-8',newline='') as handle:
        for row in csv.DictReader(handle):
            if row['prediction_timestamp']>limit:continue
            if row['churn_next_month']=='':continue
            targets[(row['customer_id'],row['prediction_timestamp'])]=(int(row['churn_next_month']),row['label_available_at'])
    rows=[]
    with (raw/'monthly_snapshots.csv').open(encoding='utf-8',newline='') as handle:
        for original in csv.DictReader(handle):
            if original['prediction_timestamp']>limit:continue
            key=(original['customer_id'],original['prediction_timestamp'])
            if key not in targets:continue
            if original['features_available_at']>=original['prediction_timestamp']:raise ValueError('Feature posterior al scoring')
            row={name:original[name] for name in POLICY['features']}
            row.update(customer_id=key[0],prediction_timestamp=key[1],target=targets[key][0],
                label_available_at=targets[key][1],mrr_usd=original['mrr_usd'])
            rows.append(row)
    if len({(r['customer_id'],r['prediction_timestamp']) for r in rows})!=len(rows):raise ValueError('Claves duplicadas')
    return rows


def run(root,output):
    output.mkdir(parents=True,exist_ok=False)
    rows=load_development(root)
    policy={**POLICY,'dataset_sha256':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((root/'data/raw').glob('*.csv'))},
        'code_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    # Congelar política en disco antes de cualquier evaluación de desarrollo.
    (output/'policy.json').write_text(json.dumps(policy,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    results=[];models={}
    for month in POLICY['development_months']:
        cutoff=month+'-01T00:00:00Z'
        train=[r for r in rows if r['prediction_timestamp']<cutoff and r['label_available_at']<=cutoff]
        val=[r for r in rows if r['prediction_timestamp']==cutoff]
        model=fit(train,cutoff);models[month]=model
        result=evaluate(predict(model,val),val,POLICY['k'])
        result.update(month=month,training_rows=len(train),last_training_prediction=max(r['prediction_timestamp'] for r in train),
            max_training_label_available_at=max(r['label_available_at'] for r in train))
        results.append(result)
    final_train=[r for r in rows if r['label_available_at']<=POLICY['final_training_timestamp']]
    final_model=fit(final_train,POLICY['final_training_timestamp'])
    summary={'scope':'desarrollo únicamente; test final no puntuado/evaluado','folds':len(results),
        'mean_precision':statistics.mean(r['precision'] for r in results),
        'mean_recall':statistics.mean(r['recall'] for r in results if r['recall'] is not None),
        'mean_lift':statistics.mean(r['lift'] for r in results if r['lift'] is not None),
        'mean_random_expected_precision':statistics.mean(r['random_expected_precision'] for r in results),
        'mean_random_expected_recall':statistics.mean(r['random_expected_recall'] for r in results if r['random_expected_recall'] is not None),
        'holdout_metrics_computed':False,'final_model_training_rows':final_model['training_rows']}
    for name,value in [('results',results),('summary',summary),('development-models',models),('final-model',final_model)]:
        (output/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description='Baseline reproducible de desarrollo del piloto')
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    run(Path(__file__).resolve().parents[1],args.output)
