"""Refit/evaluación final v0.1.0; reutiliza baseline intacto, sin tuning."""
import argparse
import csv
import hashlib
import importlib.util
import json
import os
import tempfile
from datetime import datetime, timezone
from pathlib import Path

POLICY = {
    'version': '0.1.0', 'training_cutoff': '2025-07-01',
    'scoring_start': '2025-07-01', 'scoring_end_exclusive': '2025-10-01',
    'evaluation_timestamp': '2026-01-15', 'refit_count': 1,
    'model_update_during_test': False, 'hyperparameter_search': False,
    'k': 100, 'tie_break': 'application_id ascending',
}
_BASELINE = None


def baseline():
    global _BASELINE
    if _BASELINE is None:
        path = Path(__file__).with_name('credit_baseline.py')
        spec = importlib.util.spec_from_file_location('frozen_credit_baseline', path)
        _BASELINE = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_BASELINE)
    return _BASELINE


def read_tables(root, names):
    tables = {}
    for name in names:
        with (Path(root) / 'data/raw' / (name + '.csv')).open(newline='', encoding='utf-8') as stream:
            records = list(csv.DictReader(stream))
        table = {r['application_id']: r for r in records}
        if len(table) != len(records):
            raise ValueError('Clave duplicada: ' + name)
        tables[name] = table
    first = next(iter(tables.values()))
    if any(set(t) != set(first) for t in tables.values()):
        raise ValueError('Claves de tablas no coinciden')
    return tables


def feature_row(app, history):
    if app['customer_id'] != history['customer_id']:
        raise ValueError('Cliente incompatible en join')
    row = {name: app[name] for name in baseline().POLICY['features'] if name != 'prior_late_count'}
    row.update(prior_late_count=history['prior_late_count'], history_available_at=history['available_at'],
               application_id=app['application_id'], customer_id=app['customer_id'], scoring_at=app['scoring_at'])
    baseline().check_features(row)
    return row


def load_train(root):
    tables = read_tables(root, ['applications', 'history', 'outcomes'])
    rows = []
    cutoff = POLICY['training_cutoff']
    for identifier, app in tables['applications'].items():
        # Filtrar scoring y disponibilidad ANTES de interpretar target.
        if app['scoring_at'] >= cutoff:
            continue
        label = tables['outcomes'][identifier]
        if label['label_status'] != 'observed' or not label['label_available_at'] or label['label_available_at'] > cutoff:
            continue
        if label['target_30dpd_90d'] not in ['0', '1']:
            raise ValueError('Target de train inválido')
        row = feature_row(app, tables['history'][identifier])
        row.update(target=int(label['target_30dpd_90d']), label_status='observed', label_available_at=label['label_available_at'])
        rows.append(row)
    return rows


def load_scoring(root):
    tables = read_tables(root, ['applications', 'history'])
    return [feature_row(app, tables['history'][identifier]) for identifier, app in tables['applications'].items()
            if POLICY['scoring_start'] <= app['scoring_at'] < POLICY['scoring_end_exclusive']]


def load_labels(root, requested_ids):
    tables = read_tables(root, ['outcomes'])
    if not requested_ids.issubset(tables['outcomes']):
        raise ValueError('Falta label para solicitud pedida')
    labels = {}
    for identifier in sorted(requested_ids):
        original = tables['outcomes'][identifier]
        status = original['label_status']
        available = original['label_available_at']
        observed_target = None
        if status == 'observed':
            if not available:
                raise ValueError('Label observado sin disponibilidad')
            if available <= POLICY['evaluation_timestamp']:
                if original['target_30dpd_90d'] not in ['0', '1']:
                    raise ValueError('Target de evaluación inválido')
                observed_target = int(original['target_30dpd_90d'])
            else:
                status = 'pending'
        elif status not in ['pending', 'not_observed_rejected']:
            raise ValueError('Estado de label desconocido')
        labels[identifier] = {'target': observed_target, 'label_status': status, 'label_available_at': available}
    return labels


def verify_freeze(root, freeze_file):
    frozen = json.loads(Path(freeze_file).read_text())
    expected = {'data/raw/' + n + '.csv' for n in ['applications', 'history', 'decisions', 'outcomes', 'post_decision']}
    if set(frozen['inputs']) != expected:
        raise ValueError('Freeze sin todos los inputs')
    for relative, digest in frozen['inputs'].items():
        if hashlib.sha256((Path(root) / relative).read_bytes()).hexdigest() != digest:
            raise ValueError('Input hash cambió: ' + relative)
    runner = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    base = hashlib.sha256(Path(__file__).with_name('credit_baseline.py').read_bytes()).hexdigest()
    if runner != frozen['runner_sha256'] or base != frozen['baseline_sha256']:
        raise ValueError('Código hash difiere del freeze')
    if POLICY != frozen['policy']:
        raise ValueError('policy difiere del freeze')
    return frozen


def run(root, output, freeze_file):
    root, output = Path(root), Path(output)
    if output.exists():
        raise FileExistsError('Usar un destino nuevo')
    frozen = verify_freeze(root, freeze_file)
    base = baseline()
    if base.POLICY['k'] != POLICY['k']:
        raise ValueError('Capacidad distinta del baseline aprobado')
    events = ['freeze_verified']
    train = load_train(root)
    model = base.fit(train, POLICY['training_cutoff'])
    events.append('final_refit_completed')
    scoring = load_scoring(root)
    if not scoring:
        raise ValueError('Scoring vacío')
    scores = base.predict(model, scoring)
    reference = [{'application_id': r['application_id'], 'score': model['reference_probability']} for r in scoring]
    events.append('predictions_computed_without_evaluation_labels')
    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='.credit-final-', dir=output.parent) as temp:
        stage = Path(temp)
        def write(name, data):
            (stage / (name + '.json')).write_text(json.dumps(data, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
        write('model', model)
        write('predictions', scores)
        write('reference-predictions', reference)
        events.append('predictions_persisted')
        labels = load_labels(root, {r['application_id'] for r in scoring})
        events.append('evaluation_labels_loaded')
        rows = [{**row, **labels[row['application_id']]} for row in scoring]
        evaluable = [r for r in rows if r['label_status'] == 'observed']
        ids = {r['application_id'] for r in evaluable}
        eval_scores = [s for s in scores if s['application_id'] in ids]
        eval_reference = [s for s in reference if s['application_id'] in ids]
        results = {'evaluable': {'model': base.metrics(eval_scores, evaluable),
                                'reference': base.metrics(eval_reference, evaluable),
                                **base.group_reports(eval_scores, eval_reference, train, evaluable)},
                   'all_applications_monthly': {}}
        for month in sorted({r['scoring_at'][:7] for r in rows}):
            subset = [r for r in rows if r['scoring_at'].startswith(month)]
            subset_ids = {r['application_id'] for r in subset}
            results['all_applications_monthly'][month] = base.selection([s for s in scores if s['application_id'] in subset_ids], subset, POLICY['k'])
        events.append('metrics_computed')
        m, r = results['evaluable']['model'], results['evaluable']['reference']
        summary = {'scope': 'Evaluación final sintética; calidad evaluable solo en concedidas maduras',
                   'training_rows': len(train), 'scored_rows': len(scoring), 'evaluated_rows': len(evaluable),
                   'unobserved_rejected_rows': sum(r['label_status'] == 'not_observed_rejected' for r in rows),
                   'pending_rows': sum(r['label_status'] == 'pending' for r in rows),
                   'reference_probability': model['reference_probability'],
                   'brier_model': m['brier_score'], 'brier_reference': r['brier_score'],
                   'brier_improvement': r['brier_score'] - m['brier_score'] if m['brier_score'] is not None else None,
                   'roc_auc_model': m['roc_auc'], 'final_metrics_computed': True,
                   'last_train_scoring': max(x['scoring_at'] for x in train),
                   'latest_train_label_available': max(x['label_available_at'] for x in train)}
        metadata = {'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'events': events,
                    'configuration_fixed_from_development': True,
                    'hyperparameter_search': False, 'model_updates_during_test': 0,
                    'additional_runtime_api_calls': 0, 'freeze_sha256': hashlib.sha256(Path(freeze_file).read_bytes()).hexdigest(),
                    'limits': ['Sin eficacia causal de revisión.', 'Sin métricas globales identificadas para rechazadas.',
                               'Benchmark Top-K retrospectivo, no política online.', 'Raw accesible: evaluación no ciega.']}
        write('results', results)
        write('summary', summary)
        write('evaluation-labels', labels)
        write('execution-policy', frozen)
        write('metadata', metadata)
        # Rename del directorio completo; nunca sobrescribir una ejecución existente.
        if output.exists():
            raise FileExistsError('Destino creado durante evaluación')
        os.rename(stage, output)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Refit y evaluación final con baseline congelado.')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--freeze-file', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(Path(__file__).resolve().parents[1], args.output, args.freeze_file), ensure_ascii=False, indent=2))
