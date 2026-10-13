"""Métricas de ranking y aceptación congelada; no optimiza estrategias."""
import math
import numpy as np
import pandas as pd

BASELINE='historical_sales'

def top_k(predictions,capacity):
    if isinstance(capacity,bool) or not isinstance(capacity,int) or capacity<=0:raise ValueError('capacidad inválida')
    p=predictions.copy(deep=True)
    if p.empty or p.cutoff.nunique()!=1:raise ValueError('ranking requiere un cutoff no vacío')
    if p[['customer_id','cutoff']].isna().any().any() or p.duplicated(['customer_id','cutoff']).any():raise ValueError('key inválida/repetida')
    p['customer_id']=p.customer_id.astype('string')
    if p.customer_id.str.strip().eq('').any() or p.duplicated(['customer_id','cutoff']).any():raise ValueError('ID inválido/repetido')
    if not np.isfinite(p.score.to_numpy(dtype=float)).all():raise ValueError('score no finito')
    return p.sort_values(['score','customer_id'],ascending=[False,True],kind='stable').head(capacity).reset_index(drop=True)

def ranking_metrics(predictions,outcomes,capacity):
    top_k(predictions,capacity) # Validar población completa, no solo Top-K.
    o=outcomes.copy(deep=True)
    if o.duplicated(['customer_id','cutoff']).any() or o[['customer_id','cutoff']].isna().any().any():raise ValueError('outcome key inválida/repetida')
    if 'horizon_complete' not in o or not o.horizon_complete.eq(True).all():raise ValueError('outcome sin horizonte completo')
    y=o.target_sales_90d.to_numpy(dtype=float)
    if not np.isfinite(y).all() or (y<0).any():raise ValueError('outcome inválido')
    joined=predictions.merge(o[['customer_id','cutoff','target_sales_90d']],on=['customer_id','cutoff'],how='outer',validate='one_to_one',indicator=True)
    if not joined['_merge'].eq('both').all():raise ValueError('poblaciones diferentes/outcome ausente')
    chosen=top_k(joined.drop(columns='_merge'),capacity)
    total=float(joined.target_sales_90d.sum());sales=float(chosen.target_sales_90d.sum())
    return {'effective_k':len(chosen),'eligible_count':len(joined),'top_k_sales':sales,'eligible_sales':total,'sales_share':sales/total if total>0 else None,'mae':float(np.mean(np.abs(joined.score-joined.target_sales_90d))),'top1_sales_share_within_top_k':float(chosen.target_sales_90d.nlargest(1).sum()/sales) if sales>0 else None,'top10_sales_share_within_top_k':float(chosen.target_sales_90d.nlargest(10).sum()/sales) if sales>0 else None}

def select_development(development,contract):
    periods=development['periods'];minimum=contract['development_acceptance']['minimum_periods']
    if len(periods)<minimum:raise ValueError('development insuficiente')
    if len({p['cutoff'] for p in periods})!=len(periods):raise ValueError('períodos development repetidos')
    models=[x['id'] for x in contract['models_fixed']]
    if models!=['ridge_log','hist_gradient_log']:raise ValueError('modelos no corresponden al contrato del piloto')
    values={}
    for method in [BASELINE]+models:
        try:xs=[float(p['metrics'][method]['top_k_sales']) for p in periods]
        except (KeyError,TypeError) as exc:raise ValueError('métricas development incompletas') from exc
        if not all(math.isfinite(x) and x>=0 for x in xs):raise ValueError('métricas development inválidas')
        values[method]=xs
    base=values[BASELINE];detail={}
    for method in models:
        xs=values[method];losses=sum(x<b for x,b in zip(xs,base));gain=sum(xs)>sum(base)
        detail[method]={'aggregate_sales':sum(xs),'baseline_aggregate_sales':sum(base),'losing_periods':losses,'eligible':gain and losses<=len(periods)//2}
    eligible=[m for m in models if detail[m]['eligible']]
    selected=BASELINE
    if len(eligible)==1:selected=eligible[0]
    elif len(eligible)==2:selected=models[1] if all(c>s for c,s in zip(values[models[1]],values[models[0]])) else models[0]
    return {'selected_method':selected,'period_count':len(periods),'candidate_checks':detail,'reason':'Ningún modelo elegible; mantener baseline.' if not eligible else 'Selección solo con development según contrato.'}

def acceptance_decision(development,holdout,contract):
    selection=select_development(development,contract);chosen=selection['selected_method']
    required={BASELINE,chosen}
    if not required.issubset(holdout):raise ValueError('outcome seleccionado ausente')
    amounts={m:float(holdout[m]['top_k_sales']) for m in required}
    if not all(math.isfinite(x) and x>=0 for x in amounts.values()):raise ValueError('métricas holdout inválidas')
    recommended=chosen if chosen!=BASELINE and amounts[chosen]>amounts[BASELINE] else BASELINE
    return {'development_selection':selection,'recommended_method':recommended,'holdout_rule':'Mejora estricta del seleccionado; empate/pérdida mantiene baseline sin elegir otro modelo.','scope':'Ranking retrospectivo; no uplift ni política causal de contacto.'}
