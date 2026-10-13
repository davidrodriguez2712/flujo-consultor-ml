"""Genera exclusivamente fixtures sintéticos, sin datos personales ni dependencias externas.

Uso: python analysis/generate_synthetic_data.py --output /carpeta/nueva
"""
from pathlib import Path
from datetime import date,timedelta
import argparse,csv,random

parser=argparse.ArgumentParser(description="Generador reproducible del piloto sintético de churn")
parser.add_argument("--output",required=True,type=Path)
args=parser.parse_args()
raw=args.output
if raw.exists() and any(raw.iterdir()):
    parser.error("El destino debe estar vacío; no se sobrescriben datos.")
raw.mkdir(parents=True,exist_ok=True)
SEED=20261007;rng=random.Random(SEED)
extracted=date(2026,1,15)
def month(year,number):
 return date(year+(number-1)//12,(number-1)%12+1,1)
customers=[];snapshots=[];labels=[];tickets=[]
for customer in range(1,2401):
 cid=f'SYN-{customer:05d}'
 signup=date(2023,7,1)+timedelta(days=rng.randrange(365))
 plan=rng.choice(['basic','standard','premium']);mrr={'basic':29,'standard':59,'premium':99}[plan]
 customers.append({'customer_id':cid,'signup_date':signup.isoformat(),'plan':plan,'channel':rng.choice(['organic','paid','partner']),'market':'synthetic','is_synthetic':1})
 affinity=rng.uniform(.35,.95);previous_usage=max(1,round(26*affinity))
 cancelled=False;first_snapshot=True
 for offset in range(24):
  cutoff=month(2024,2+offset);end=month(2024,3+offset);prev=month(2024,1+offset)
  if cutoff<=signup or cancelled:continue
  tenure=(cutoff.year-signup.year)*12+cutoff.month-signup.month
  prev2=month(2024,offset)
  if first_snapshot:
   previous_usage=min(previous_usage,max(0,(prev-max(prev2,signup)).days))
  observable_days=(cutoff-max(prev,signup)).days
  disengaged=rng.random()<.16
  usage=max(0,min((cutoff-prev).days,round(previous_usage*.5+rng.gauss(13*affinity,3))))
  usage=min(usage,observable_days)
  if disengaged:usage=round(usage*rng.uniform(.1,.55))
  failed=int(rng.random()<.08)+int(rng.random()<.015)
  ntickets=int(rng.random()<.22)+int(rng.random()<.08)+int(rng.random()<.025)
  ratio=usage/max(1,previous_usage)
  prob=min(.65,.008+.14*max(0,1-ratio)+.065*failed+.025*ntickets+.012*(tenure<3))
  churn=int(rng.random()<prob)
  cancellation=cutoff+timedelta(days=rng.randrange((end-cutoff).days)) if churn else None
  available=end+timedelta(days=7)
  observed=available<=extracted
  snapshots.append({'customer_id':cid,'prediction_timestamp':cutoff.isoformat()+'T00:00:00Z','features_available_at':(cutoff-timedelta(days=1)).isoformat()+'T23:00:00Z','tenure_months':tenure,'active_days_prev_month':'' if rng.random()<.02 else usage,'active_days_prev2_month':previous_usage,'failed_payments_prev_month':failed,'support_tickets_prev_month':ntickets,'mrr_usd':mrr,'discount_active':int(rng.random()<.1),'is_synthetic':1})
  labels.append({'customer_id':cid,'prediction_timestamp':cutoff.isoformat()+'T00:00:00Z','window_end_exclusive':end.isoformat()+'T00:00:00Z','label_available_at':available.isoformat()+'T00:00:00Z','churn_next_month':churn if observed else '', 'label_status':'observed' if observed else 'pending','cancellation_at':cancellation.isoformat()+'T12:00:00Z' if cancellation and cancellation<extracted else '', 'extracted_at':extracted.isoformat()+'T00:00:00Z','is_synthetic':1})
  for t in range(ntickets):
   day=max(prev,signup)+timedelta(days=rng.randrange(observable_days))
   tickets.append({'ticket_id':f'T-{len(tickets)+1:07d}','customer_id':cid,'snapshot_prediction_timestamp':cutoff.isoformat()+'T00:00:00Z','opened_at':day.isoformat()+'T12:00:00Z','category':rng.choice(['billing','technical','account']),'is_synthetic':1})
  previous_usage=usage;cancelled=bool(churn);first_snapshot=False

def write_csv(name,rows):
 with (raw/name).open('x',newline='',encoding='utf-8') as out:
  writer=csv.DictWriter(out,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
for name,rows in [('customers.csv',customers),('monthly_snapshots.csv',snapshots),('churn_labels.csv',labels),('support_tickets.csv',tickets)]:write_csv(name,rows)

import json,hashlib
manifest={"generator_version":"2","generator_sha256":hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),"seed":SEED,"is_synthetic":True,"extracted_at":str(extracted),"files":{p.name:{"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size} for p in sorted(raw.glob("*.csv"))}}
(raw/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print(json.dumps({"output":str(raw),"rows":{"customers":len(customers),"monthly_snapshots":len(snapshots),"churn_labels":len(labels),"support_tickets":len(tickets)}}))
