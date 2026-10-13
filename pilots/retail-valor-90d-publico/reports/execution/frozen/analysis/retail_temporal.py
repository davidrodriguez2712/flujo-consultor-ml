"""Snapshots históricos reproducibles; no entrenan ni eligen modelos."""
import numpy as np
import pandas as pd

FEATURES=['recency_days','orders_90d','orders_180d','sales_90d','sales_180d',
          'units_180d','distinct_products_180d','tenure_observed_days']

def reconcile_transactions(frame,contract):
    """Conservar máxima multiplicidad entre hojas y mapa de copias descartadas."""
    f=frame.copy(deep=True);f.attrs={}
    fields=contract['reconciliation']['fields']
    f['_occurrence']=f.groupby(['source_sheet']+fields,dropna=False,sort=False).cumcount()
    keys=fields+['_occurrence']
    dup=f.duplicated(keys,keep='first')
    representatives=f.loc[~dup,keys+['source_sheet','source_row']].rename(columns={'source_sheet':'kept_source_sheet','source_row':'kept_source_row'})
    mapping=f.loc[dup,keys+['source_sheet','source_row']].merge(representatives,on=keys,how='left',validate='many_to_one')
    out=f.loc[~dup].drop(columns='_occurrence').reset_index(drop=True)
    out.attrs['copy_map']=mapping.drop(columns='_occurrence')
    return out

def valid_purchases(frame,contract):
    """Filtros ordenados con razones excluyentes y provenance conservada."""
    f=frame.copy(deep=True);f.attrs={}
    reason=pd.Series('',index=f.index,dtype='string')
    def mark(mask,name):reason.loc[(reason=='')&mask.fillna(True)]=name
    required=['invoice_id','stock_code','invoice_at','quantity','unit_price']
    bad=f[required].isna().any(axis=1)|~np.isfinite(f.quantity)|~np.isfinite(f.unit_price)
    mark(bad,'required_or_nonfinite')
    mark(f.invoice_id.astype('string').str.match('^[cC]',na=False),'cancellation')
    mark((f.quantity<=0)|(f.unit_price<=0),'nonpositive')
    mark(~f.stock_code.astype('string').str.fullmatch(contract['purchase_validity']['stock_code_regex'],na=False),'nonstandard_code')
    mark(f.customer_id.isna()|f.customer_id.astype('string').str.strip().eq(''),'missing_customer_id')
    excluded=f.loc[reason!=''].copy();excluded['exclusion_reason']=reason.loc[reason!='']
    out=f.loc[reason==''].copy();out.attrs['excluded']=excluded
    return out

def build_snapshot(frame,cutoff,contract,observed_until,observed_from=None):
    t=pd.Timestamp(cutoff);end=t+pd.Timedelta(days=contract['horizon_days'])
    start=t-pd.Timedelta(days=contract['history_days']);recent=t-pd.Timedelta(days=contract['baseline_days'])
    if pd.Timestamp(observed_until)<end:raise ValueError('horizonte incompleto')
    earliest=pd.Timestamp(observed_from) if observed_from is not None else frame.invoice_at.min()
    if pd.isna(earliest) or earliest>start:raise ValueError('historia incompleta')
    v=valid_purchases(frame,contract);v.attrs={};v['amount']=v.quantity*v.unit_price
    h=v.loc[(v.invoice_at>=start)&(v.invoice_at<t)]
    cols=['customer_id','cutoff','label_end','target_sales_90d']+FEATURES+['history_min_at','history_max_at','target_min_at','target_max_at']
    if h.empty:return pd.DataFrame(columns=cols)
    g=h.groupby('customer_id',sort=True)
    s=g.agg(orders_180d=('invoice_id','nunique'),sales_180d=('amount','sum'),units_180d=('quantity','sum'),distinct_products_180d=('stock_code','nunique'),history_min_at=('invoice_at','min'),history_max_at=('invoice_at','max'))
    s['recency_days']=(t-s.history_max_at).dt.total_seconds()/86400
    r=h.loc[h.invoice_at>=recent].groupby('customer_id').agg(orders_90d=('invoice_id','nunique'),sales_90d=('amount','sum'))
    s=s.join(r,validate='one_to_one');s[['orders_90d','sales_90d']]=s[['orders_90d','sales_90d']].fillna(0)
    first=v.loc[v.invoice_at<t].groupby('customer_id').invoice_at.min()
    s['tenure_observed_days']=(t-first.reindex(s.index)).dt.total_seconds()/86400
    future=v.loc[(v.invoice_at>=t)&(v.invoice_at<end)].groupby('customer_id').agg(target_sales_90d=('amount','sum'),target_min_at=('invoice_at','min'),target_max_at=('invoice_at','max'))
    s=s.join(future,validate='one_to_one');s['target_sales_90d']=s.target_sales_90d.fillna(0)
    s['cutoff']=t;s['label_end']=end
    return s.reset_index()[cols]

def training_rows(snapshots,fit_at):
    fit=pd.Timestamp(fit_at)
    return snapshots.loc[(snapshots.label_end<=fit)&(snapshots.cutoff<fit)].copy()
