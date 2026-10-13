"""Regresiones: seed, labels, fechas, claves y preservación de inputs."""
import csv
import importlib.util
from datetime import date, timedelta
from pathlib import Path
import pytest

MODULE = Path(__file__).with_name('generate_synthetic_data.py')

def generator():
    assert MODULE.is_file(), 'Falta implementar el generator'
    spec = importlib.util.spec_from_file_location('credit_generator', MODULE)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def rows(root, name):
    with (root / name).open(newline='') as stream:
        return list(csv.DictReader(stream))

def test_same_seed_reproduces_csv_bytes(tmp_path):
    gen = generator()
    gen.generate(tmp_path / 'a')
    gen.generate(tmp_path / 'b')
    for path in (tmp_path / 'a').glob('*.csv'):
        assert path.read_bytes() == (tmp_path / 'b' / path.name).read_bytes()
    gen.generate(tmp_path / 'c', seed=19)
    assert (tmp_path / 'a/applications.csv').read_bytes() != (tmp_path / 'c/applications.csv').read_bytes()

def test_rejections_have_no_observed_outcome(tmp_path):
    generator().generate(tmp_path)
    decisions = {r['application_id']: r for r in rows(tmp_path, 'decisions.csv')}
    outcomes = rows(tmp_path, 'outcomes.csv')
    rejected = [r for r in outcomes if decisions[r['application_id']]['decision'] == 'rejected']
    assert rejected
    assert all(r['label_status'] == 'not_observed_rejected' and r['target_30dpd_90d'] == '' and r['label_available_at'] == '' for r in rejected)

def test_pending_is_not_zero_and_full_labels_follow_97_day_rule(tmp_path):
    generator().generate(tmp_path)
    outcomes = rows(tmp_path, 'outcomes.csv')
    pending = [r for r in outcomes if r['label_status'] == 'pending']
    observed = [r for r in outcomes if r['label_status'] == 'observed']
    assert pending and observed
    assert all(r['target_30dpd_90d'] == '' and r['label_available_at'] > '2026-01-15' for r in pending)
    assert {r['target_30dpd_90d'] for r in observed} == {'0', '1'}
    for r in pending + observed:
        assert date.fromisoformat(r['window_end']) == date.fromisoformat(r['disbursed_at']) + timedelta(days=90)
        assert date.fromisoformat(r['label_available_at']) == date.fromisoformat(r['disbursed_at']) + timedelta(days=97)
        assert (r['label_status'] == 'observed') == (r['label_available_at'] <= '2026-01-15')

def test_keys_repeated_clients_and_predecision_history(tmp_path):
    generator().generate(tmp_path)
    apps = rows(tmp_path, 'applications.csv')
    assert len(apps) == 7200
    ids = {r['application_id'] for r in apps}
    assert len(ids) == len(apps)
    assert len({r['customer_id'] for r in apps}) < len(apps)
    appmap = {r['application_id']: r for r in apps}
    for name in ['history.csv', 'decisions.csv', 'outcomes.csv', 'post_decision.csv']:
        table = rows(tmp_path, name)
        assert len(table) == len(apps) and {r['application_id'] for r in table} == ids
    for r in rows(tmp_path, 'history.csv'):
        assert r['available_at'] <= appmap[r['application_id']]['scoring_at']

def test_postdecision_leakage_columns_are_late_and_absent_when_pending(tmp_path):
    generator().generate(tmp_path)
    apps = {r['application_id']: r for r in rows(tmp_path, 'applications.csv')}
    outcomes = {r['application_id']: r for r in rows(tmp_path, 'outcomes.csv')}
    for r in rows(tmp_path, 'post_decision.csv'):
        if outcomes[r['application_id']]['label_status'] == 'observed':
            assert r['available_at'] > apps[r['application_id']]['scoring_at']
            assert r['max_dpd_90d'] != ''
            assert (int(r['max_dpd_90d']) >= 30) == (outcomes[r['application_id']]['target_30dpd_90d'] == '1')
        else:
            assert r['max_dpd_90d'] == '' and r['available_at'] == ''

def test_generator_refuses_to_overwrite_sources(tmp_path):
    gen = generator()
    gen.generate(tmp_path)
    before = (tmp_path / 'applications.csv').read_bytes()
    with pytest.raises(FileExistsError):
        gen.generate(tmp_path, seed=2)
    assert (tmp_path / 'applications.csv').read_bytes() == before
