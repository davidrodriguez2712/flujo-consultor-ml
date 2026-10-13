"""Fixture de laboratorio v0.1.0, stdlib, sin datos de clientes reales."""
import argparse
import csv
import hashlib
import json
import math
import random
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

EXTRACT = date(2026, 1, 15)
VERSION = '0.1.0'

def generate(output: Path, seed: int = 20261008):
    output = Path(output)
    names = ['applications', 'history', 'decisions', 'outcomes', 'post_decision']
    targets = [output / (name + '.csv') for name in names] + [output / 'manifest.json']
    if any(p.exists() for p in targets):
        raise FileExistsError('No sobrescribir fuentes; usar un directorio nuevo.')
    rng = random.Random(seed)
    # La propensión latente persiste por cliente; no se exporta como feature.
    clients = {f'C{i:04d}': (rng.uniform(-1, 1), rng.randint(900, 5500)) for i in range(1, 1801)}
    tables = {name: [] for name in names}
    for month_index in range(24):
        year, month = 2024 + month_index // 12, month_index % 12 + 1
        for index in range(300):
            identifier = f'A{month_index * 300 + index + 1:06d}'
            customer = rng.choice(list(clients))
            latent, base_income = clients[customer]
            scoring = date(year, month, rng.randint(1, 28))
            income = max(600, round(base_income + rng.gauss(0, 150)))
            dti = round(rng.uniform(.05, .75), 4)
            amount = rng.randrange(1000, 20001, 100)
            bureau = max(300, min(850, round(650 - latent * 70 - dti * 80 + rng.gauss(0, 45))))
            prior_late = max(0, round(latent + dti * 2 + rng.gauss(0, .8)))
            decision_date = scoring + timedelta(days=1)
            # Política histórica ficticia: no es una recomendación de aprobación.
            approval_prob = 1 / (1 + math.exp(-((bureau - 580) / 55 - 2 * dti)))
            approved = rng.random() < approval_prob
            tables['applications'].append(dict(application_id=identifier, customer_id=customer, scoring_at=scoring.isoformat(), monthly_income=income, debt_to_income=dti, requested_amount=amount, bureau_score=bureau))
            tables['history'].append(dict(application_id=identifier, customer_id=customer, snapshot_at=(scoring - timedelta(days=10)).isoformat(), available_at=(scoring - timedelta(days=2)).isoformat(), prior_late_count=prior_late))
            tables['decisions'].append(dict(application_id=identifier, decision_at=decision_date.isoformat(), decision='approved' if approved else 'rejected', funded_amount=amount if approved else '', disbursed_at=decision_date.isoformat() if approved else ''))
            end = decision_date + timedelta(days=90)
            available = decision_date + timedelta(days=97)
            status = 'not_observed_rejected' if not approved else ('observed' if available <= EXTRACT else 'pending')
            target = ''
            max_dpd = ''
            if status == 'observed':
                probability = 1 / (1 + math.exp(-(-3 + 1.1 * latent + 2 * dti + .25 * prior_late + (620 - bureau) / 150 + .2 * month_index / 23)))
                target = int(rng.random() < probability)
                max_dpd = rng.randint(30, 90) if target else rng.randint(0, 29)
            tables['outcomes'].append(dict(application_id=identifier, extract_at=EXTRACT.isoformat(), disbursed_at=decision_date.isoformat() if approved else '', window_end=end.isoformat() if approved else '', label_available_at=available.isoformat() if approved else '', label_status=status, target_30dpd_90d=target))
            tables['post_decision'].append(dict(application_id=identifier, available_at=available.isoformat() if status == 'observed' else '', max_dpd_90d=max_dpd))
    output.mkdir(parents=True, exist_ok=True)
    files = {}
    for name, data in tables.items():
        path = output / (name + '.csv')
        with path.open('w', newline='', encoding='utf-8') as stream:
            writer = csv.DictWriter(stream, fieldnames=list(data[0]))
            writer.writeheader()
            writer.writerows(data)
        files[path.name] = {'rows': len(data), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'bytes': path.stat().st_size}
    observed = [r for r in tables['outcomes'] if r['label_status'] == 'observed']
    manifest = dict(generator_version=VERSION, seed=seed, synthetic=True, extract_at=EXTRACT.isoformat(), files=files, applications=7200, unique_customers=len({r['customer_id'] for r in tables['applications']}), label_counts=dict(Counter(r['label_status'] for r in tables['outcomes'])), observed_positives=sum(r['target_30dpd_90d'] for r in observed), generator_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generar datos de crédito sintéticos en un directorio nuevo.')
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1] / 'data/raw')
    parser.add_argument('--seed', type=int, default=20261008)
    args = parser.parse_args()
    print(json.dumps(generate(args.output, args.seed), ensure_ascii=False, indent=2))
