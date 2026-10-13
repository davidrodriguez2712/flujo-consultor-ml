"""Forecast semanal del piloto: operaciones deterministas, sin dependencias externas."""
from collections import defaultdict
from datetime import datetime,timedelta,date
from decimal import Decimal
import math

METHODS=('previous_week','mean_previous_4_weeks')


def monday(day):
    return day-timedelta(days=day.weekday())


def build_weekly(rows):
    orders=defaultdict(set)
    invoice_weeks=defaultdict(set)
    raw_count=qualified_count=0
    earliest=latest=None
    for row in rows:
        raw_count+=1
        day=datetime.fromisoformat(row['invoice_at']).date()
        earliest=day if earliest is None else min(earliest,day)
        latest=day if latest is None else max(latest,day)
        quantity,price=Decimal(row['quantity']),Decimal(row['unit_price'])
        if not quantity.is_finite() or not price.is_finite():
            raise ValueError('Cantidad o precio no finito.')
        invoice=row['invoice_id'].strip()
        if row['country']=='United Kingdom' and invoice and not invoice.upper().startswith('C') and quantity>0 and price>0:
            week=monday(day)
            orders[week].add(invoice)
            invoice_weeks[invoice].add(week)
            qualified_count+=1
    if earliest is None:
        raise ValueError('Fuente vacía.')
    first,last=monday(earliest),monday(latest)
    # Ambas semanas de frontera se excluyen por cobertura parcial del extract.
    week=first+timedelta(days=7)
    output=[]
    while week<last:
        output.append({'cutoff':week.isoformat(),'week_end_exclusive':(week+timedelta(days=7)).isoformat(),'actual':len(orders[week])})
        week+=timedelta(days=7)
    return output,{'raw_rows':raw_count,'qualifying_item_rows':qualified_count,'min_date':earliest.isoformat(),'max_date':latest.isoformat(),'first_partial_week':first.isoformat(),'last_partial_week':last.isoformat(),'complete_calendar_weeks':len(output),'qualifying_invoice_ids_multiple_weeks':sum(len(w)>1 for w in invoice_weeks.values()),'zero_order_weeks':sum(r['actual']==0 for r in output),'completeness_assumption':'Cobertura del calendario interior; no se verificó completitud operativa externa.'}


def forecasts(rows,start,end,methods):
    if not methods or any(m not in METHODS for m in methods):
        raise ValueError('Método no contratado.')
    ordered=sorted(rows,key=lambda r:date.fromisoformat(r['cutoff']))
    cutoffs=[date.fromisoformat(r['cutoff']) for r in ordered]
    if len(set(cutoffs))!=len(cutoffs) or any((b-a).days!=7 for a,b in zip(cutoffs,cutoffs[1:])):
        raise ValueError('Weeks duplicadas o calendario discontinuo.')
    output=[]
    for i,row in enumerate(ordered):
        if start<=row['cutoff']<end:
            if i<4:
                raise ValueError('Historia insuficiente de cuatro semanas.')
            history=ordered[i-4:i]
            for method in methods:
                prediction=float(history[-1]['actual']) if method=='previous_week' else sum(r['actual'] for r in history)/4
                output.append({'cutoff':row['cutoff'],'week_end_exclusive':row['week_end_exclusive'],'method':method,'actual':row['actual'],'prediction':prediction})
    if not output:
        raise ValueError('No hay semanas de evaluación.')
    return output


def metrics(rows):
    if not rows or any(not math.isfinite(float(r[k])) for r in rows for k in ('actual','prediction')):
        raise ValueError('Resultados vacíos o no finitos.')
    total=sum(r['actual'] for r in rows)
    if total<=0:
        raise ValueError('Denominador de WAPE no positivo.')
    errors=[r['prediction']-r['actual'] for r in rows]
    absolute=sum(abs(x) for x in errors)
    return {'weeks':len(rows),'actual_total':total,'WAPE':absolute/total,'MAE':absolute/len(rows),'bias':sum(errors)/len(rows)}


def choose_method(results):
    return 'mean_previous_4_weeks' if results['mean_previous_4_weeks']['WAPE']<results['previous_week']['WAPE'] else 'previous_week'
