"""Dos baselines y dos modelos fijos; scoring no consume outcomes."""
import numpy as np
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.ensemble import HistGradientBoostingRegressor
from retail_temporal import FEATURES

MODEL_IDS=('historical_sales','rfm','ridge_log','hist_gradient_log')

def fit_predict(train,score_rows,model_id,seed):
    if model_id not in MODEL_IDS:raise ValueError('modelo inesperado')
    if train.empty or score_rows.empty:raise ValueError('entrenamiento/scoring vacío')
    if score_rows.duplicated(['customer_id','cutoff']).any() or score_rows.customer_id.isna().any():raise ValueError('key scoring inválida')
    if score_rows.cutoff.nunique()!=1:raise ValueError('scoring requiere un cutoff')
    cutoff=score_rows.cutoff.iloc[0]
    if (train.label_end>cutoff).any() or (train.cutoff>=cutoff).any():raise ValueError('labels no maduras al fit')
    x=train[FEATURES].to_numpy(dtype=float);z=score_rows[FEATURES].to_numpy(dtype=float)
    if not np.isfinite(x).all() or not np.isfinite(z).all():raise ValueError('features no finitas')
    y=train.target_sales_90d.to_numpy(dtype=float)
    if not np.isfinite(y).all() or (y<0).any():raise ValueError('target inválido')
    if model_id=='historical_sales':scores=score_rows.sales_90d.to_numpy(dtype=float)
    elif model_id=='rfm':
        scores=(((-score_rows.recency_days).rank(pct=True,method='average')+score_rows.orders_180d.rank(pct=True,method='average')+score_rows.sales_180d.rank(pct=True,method='average'))/3).to_numpy()
    else:
        if model_id=='ridge_log':model=make_pipeline(StandardScaler(),Ridge(alpha=1))
        else:model=HistGradientBoostingRegressor(learning_rate=0.1,max_iter=100,max_leaf_nodes=15,min_samples_leaf=20,early_stopping=False,random_state=seed)
        model.fit(x,np.log1p(y));scores=np.maximum(0,np.expm1(model.predict(z)))
    if not np.isfinite(scores).all():raise ValueError('scores no finitos')
    out=score_rows[['customer_id','cutoff']].reset_index(drop=True).copy();out['score']=scores
    return out
