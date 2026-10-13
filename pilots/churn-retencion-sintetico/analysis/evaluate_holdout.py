"""Evaluación autorizada del holdout con modelo fijo; no entrena ni modifica policy."""
import argparse
import csv
import hashlib
import json
import statistics
from pathlib import Path

import baseline


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_frozen(root):
    folder=root/'analysis/outputs/baseline-development'
    policy=json.loads((folder/'policy.json').read_text())
    audit=json.loads((root/'analysis/outputs/baseline-audit.json').read_text())
    for name,expected in audit['output_sha256'].items():
        if sha(folder/name)!=expected:raise ValueError('Hash de artefacto congelado cambió: '+name)
    for name,expected in policy['dataset_sha256'].items():
        if sha(root/'data/raw'/name)!=expected:raise ValueError('Hash de datos cambió: '+name)
    if sha(root/'analysis/baseline.py')!=policy['code_sha256']:raise ValueError('Hash del baseline cambió')
    for field in ['features','k','activity_drop_fraction','prior_strength','holdout_months','final_training_timestamp']:
        if policy[field]!=baseline.POLICY[field]:raise ValueError('Policy distinta: '+field)
    return policy,json.loads((folder/'final-model.json').read_text())


def load_holdout(root):
    months=set(baseline.POLICY['holdout_months']);raw=root/'data/raw'
    targets={}
    with (raw/'churn_labels.csv').open(newline='',encoding='utf-8') as f:
        for row in csv.DictReader(f):
            if row['prediction_timestamp'][:7] not in months:continue
            key=(row['customer_id'],row['prediction_timestamp'])
            if key in targets:raise ValueError('Clave de label duplicada')
            if row['churn_next_month']=='':raise ValueError('Label pendiente en holdout')
            target=int(row['churn_next_month'])
            if target not in (0,1):raise ValueError('Label no binaria')
            if row['label_available_at']>'2026-01-15T00:00:00Z':raise ValueError('Label no disponible en extracción')
            targets[key]=(target,row['label_available_at'])
    rows=[];keys=set()
    with (raw/'monthly_snapshots.csv').open(newline='',encoding='utf-8') as f:
        for original in csv.DictReader(f):
            if original['prediction_timestamp'][:7] not in months:continue
            key=(original['customer_id'],original['prediction_timestamp'])
            if key in keys:raise ValueError('Clave de snapshot duplicada')
            keys.add(key)
            if key not in targets:raise ValueError('Snapshot sin label')
            if original['features_available_at']>=key[1]:raise ValueError('Feature no disponible al scoring')
            row={name:original[name] for name in baseline.POLICY['features']}
            row.update(customer_id=key[0],prediction_timestamp=key[1],target=targets[key][0],
                label_available_at=targets[key][1],mrr_usd=original['mrr_usd'])
            rows.append(row)
    if keys!=set(targets):raise ValueError('Diferencia de claves snapshots/labels')
    return rows


def run(root,output):
    if output.exists():raise FileExistsError('Destino existente; no sobrescribir evaluación')
    policy,model=verify_frozen(root)
    rows=load_holdout(root)
    scores=[]
    # Persistir scoring antes de calcular métricas, usando un único modelo sin fit.
    for month in policy['holdout_months']:
        batch=[r for r in rows if r['prediction_timestamp']==month+'-01T00:00:00Z']
        if not batch:raise ValueError('Mes vacío: '+month)
        scores.extend({**s,'month':month} for s in baseline.predict(model,batch))
    output.mkdir(parents=True,exist_ok=False)
    metadata={'protocol':'modelo fijo; evaluación final sin refit ni tuning',
        'model_sha256':sha(root/'analysis/outputs/baseline-development/final-model.json'),
        'policy_sha256':sha(root/'analysis/outputs/baseline-development/policy.json'),
        'runner_sha256':sha(Path(__file__)),'training_timestamp':model['training_timestamp'],
        'training_rows':model['training_rows'],'pending_january_excluded':True}
    def write(name,value):
        (output/(name+'.json')).write_text(json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n')
    write('metadata',metadata);write('scores',scores)
    results=[]
    for month in policy['holdout_months']:
        batch=[r for r in rows if r['prediction_timestamp']==month+'-01T00:00:00Z']
        metrics=baseline.evaluate([s for s in scores if s['month']==month],batch,policy['k'])
        results.append({**metrics,'month':month})
    summary={name:statistics.mean(r[field] for r in results) for name,field in [
        ('mean_precision','precision'),('mean_recall','recall'),('mean_lift','lift'),
        ('mean_random_expected_precision','random_expected_precision'),('mean_random_expected_recall','random_expected_recall')]}
    summary.update(months=len(results),rows=len(rows),selected_customer_months=sum(r['k_effective'] for r in results),
        hits=sum(r['hits'] for r in results),holdout_metrics_computed=True,scope='holdout sintético julio–diciembre 2025')
    write('results',results);write('summary',summary)
    print(json.dumps(summary,ensure_ascii=False))


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    run(Path(__file__).resolve().parents[1],args.output)
