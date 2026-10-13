"""Regresiones de exclusión temporal e integridad del test final."""
import csv
import shutil
from pathlib import Path

import pytest
import evaluate_holdout as runner


def fixture(root, pending=False, duplicate=False, late=False):
    raw=root/'data/raw';raw.mkdir(parents=True)
    snapshots=[];labels=[]
    for month in ['2025-06','2025-07','2025-12','2026-01']:
        timestamp=month+'-01T00:00:00Z'
        snapshots.append(dict(customer_id='A',prediction_timestamp=timestamp,
            features_available_at=timestamp if late else '2025-05-31T23:00:00Z',
            active_days_prev_month='4',active_days_prev2_month='8',
            failed_payments_prev_month='0',support_tickets_prev_month='1',mrr_usd='29'))
        labels.append(dict(customer_id='A',prediction_timestamp=timestamp,
            churn_next_month='' if pending or month in ['2025-06','2026-01'] else '1',
            label_available_at='2026-01-08T00:00:00Z'))
    if duplicate:labels.append(labels[1].copy())
    for name,rows in [('monthly_snapshots',snapshots),('churn_labels',labels)]:
        with (raw/(name+'.csv')).open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)


def test_only_july_through_december_loaded(tmp_path):
    fixture(tmp_path)
    rows=runner.load_holdout(tmp_path)
    assert [r['prediction_timestamp'] for r in rows]==['2025-07-01T00:00:00Z','2025-12-01T00:00:00Z']
    assert [r['target'] for r in rows]==[1,1]


def test_pending_holdout_label_rejected(tmp_path):
    fixture(tmp_path,pending=True)
    with pytest.raises(ValueError,match='pendiente'):runner.load_holdout(tmp_path)


def test_duplicate_label_key_rejected(tmp_path):
    fixture(tmp_path,duplicate=True)
    with pytest.raises(ValueError,match='duplicada'):runner.load_holdout(tmp_path)


def test_unavailable_feature_rejected(tmp_path):
    fixture(tmp_path,late=True)
    with pytest.raises(ValueError,match='Feature'):runner.load_holdout(tmp_path)


def test_modified_frozen_model_rejected(tmp_path):
    project=Path(__file__).resolve().parents[1]
    for name in ['analysis/outputs/baseline-development','data/raw']:
        shutil.copytree(project/name,tmp_path/name)
    (tmp_path/'analysis/baseline.py').write_bytes((project/'analysis/baseline.py').read_bytes())
    (tmp_path/'analysis/outputs/baseline-audit.json').write_bytes((project/'analysis/outputs/baseline-audit.json').read_bytes())
    runner.verify_frozen(tmp_path)
    model=tmp_path/'analysis/outputs/baseline-development/final-model.json'
    model.write_text(model.read_text()+' ')
    with pytest.raises(ValueError,match='Hash'):runner.verify_frozen(tmp_path)
