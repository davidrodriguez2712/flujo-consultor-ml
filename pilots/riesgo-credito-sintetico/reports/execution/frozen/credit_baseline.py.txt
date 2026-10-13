"""Baseline de development v0.1.0; stdlib, sin evaluación final ni tuning."""
import argparse
import csv
import hashlib
import json
import math
import statistics
from pathlib import Path

POLICY = {
    'version': '0.1.0', 'algorithm': 'standardized_logistic_regression_l2',
    'features': ['monthly_income', 'debt_to_income', 'requested_amount', 'bureau_score', 'prior_late_count'],
    'iterations': 600, 'learning_rate': .05, 'l2': .01,
    'training_cutoff': '2025-01-01', 'validation_start': '2025-01-01',
    'validation_end_exclusive': '2025-03-01', 'evaluation_timestamp': '2025-06-15',
    'calibration_bins': [0., .1, .2, .4, .6, .8, 1.], 'k': 100,
    'hyperparameter_search': False, 'final_evaluation': False,
}


def number(value):
    if value is None or value == '':
        return None
    if isinstance(value, bool):
        raise ValueError('Feature numérica inválida')
    result = float(value)
    if not math.isfinite(result):
        raise ValueError('Feature no finita')
    return result


def check_features(row):
    if not row.get('application_id') or not row.get('scoring_at'):
        raise ValueError('Falta identidad o scoring')
    if not row.get('history_available_at') or row['history_available_at'] > row['scoring_at']:
        raise ValueError('Historia no disponible al scoring')
    for feature in POLICY['features']:
        if feature not in row:
            raise ValueError('Falta feature: ' + feature)
        number(row[feature])


def target(row):
    if row.get('label_status') != 'observed' or type(row.get('target')) is not int or row['target'] not in (0, 1):
        raise ValueError('Target binario observado requerido')
    return row['target']


def vector(model, row):
    result = []
    for name in POLICY['features']:
        value = number(row[name])
        value = model['medians'][name] if value is None else value
        result.append((value - model['means'][name]) / model['scales'][name])
    return result


def sigmoid(value):
    return 1 / (1 + math.exp(-max(-35., min(35., value))))


def fit(rows, training_cutoff):
    if not rows:
        raise ValueError('Train vacío')
    if len({r['application_id'] for r in rows}) != len(rows):
        raise ValueError('Train con IDs duplicados')
    for row in rows:
        check_features(row)
        target(row)
        if row['scoring_at'] >= training_cutoff:
            raise ValueError('Scoring no anterior al fit')
        if not row.get('label_available_at') or row['label_available_at'] > training_cutoff:
            raise ValueError('Label no disponible al fit')
    model = {'version': POLICY['version'], 'training_cutoff': training_cutoff, 'training_rows': len(rows),
             'reference_probability': statistics.mean(target(r) for r in rows),
             'medians': {}, 'means': {}, 'scales': {}, 'weights': [0.] * len(POLICY['features'])}
    for name in POLICY['features']:
        values = [number(r[name]) for r in rows]
        observed = [v for v in values if v is not None]
        if not observed:
            raise ValueError('Feature completamente ausente: ' + name)
        median = statistics.median(observed)
        filled = [median if v is None else v for v in values]
        model['medians'][name] = median
        model['means'][name] = statistics.mean(filled)
        model['scales'][name] = statistics.pstdev(filled) or 1.
    p = max(1e-6, min(1 - 1e-6, model['reference_probability']))
    model['intercept'] = math.log(p / (1 - p))
    data = [(vector(model, r), target(r)) for r in rows]
    for _ in range(POLICY['iterations']):
        intercept_gradient = 0.
        gradients = [0.] * len(model['weights'])
        for features, label in data:
            error = sigmoid(model['intercept'] + sum(w * x for w, x in zip(model['weights'], features))) - label
            intercept_gradient += error
            for index, value in enumerate(features):
                gradients[index] += error * value
        model['intercept'] -= POLICY['learning_rate'] * intercept_gradient / len(data)
        model['weights'] = [w - POLICY['learning_rate'] * (g / len(data) + POLICY['l2'] * w) for w, g in zip(model['weights'], gradients)]
    return model


def predict(model, rows):
    scores = []
    for row in rows:
        check_features(row)
        value = model['intercept'] + sum(w * x for w, x in zip(model['weights'], vector(model, row)))
        scores.append({'application_id': row['application_id'], 'score': sigmoid(value)})
    return scores


def aligned(scores, rows):
    lookup = {r['application_id']: r for r in rows}
    if len(lookup) != len(rows) or len({s['application_id'] for s in scores}) != len(scores):
        raise ValueError('IDs duplicados')
    if len(scores) != len(rows) or {s['application_id'] for s in scores} != set(lookup):
        raise ValueError('Scores y población no coinciden')
    for score in scores:
        value = score['score']
        if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or not 0 <= value <= 1:
            raise ValueError('Score inválido')
    return lookup


def metrics(scores, rows):
    lookup = aligned(scores, rows)
    pairs = [(s['score'], target(lookup[s['application_id']])) for s in scores]
    brier = statistics.mean((p - y) ** 2 for p, y in pairs) if pairs else None
    positives = sum(y for _, y in pairs)
    negatives = len(pairs) - positives
    auc = None
    if positives and negatives:
        ordered = sorted(pairs)
        rank_sum = 0.
        index = 0
        while index < len(ordered):
            end = index + 1
            while end < len(ordered) and ordered[end][0] == ordered[index][0]:
                end += 1
            rank_sum += ((index + 1 + end) / 2) * sum(y for _, y in ordered[index:end])
            index = end
        auc = (rank_sum - positives * (positives + 1) / 2) / (positives * negatives)
    calibration = []
    bins = POLICY['calibration_bins']
    for index, (low, high) in enumerate(zip(bins, bins[1:])):
        group = [(p, y) for p, y in pairs if low <= p < high or (index == len(bins) - 2 and p == 1.)]
        calibration.append({'low': low, 'high': high, 'rows': len(group),
                            'mean_score': statistics.mean(p for p, _ in group) if group else None,
                            'positive_rate': statistics.mean(y for _, y in group) if group else None})
    return {'rows': len(pairs), 'positives': positives, 'brier_score': brier, 'roc_auc': auc,
            'mean_score': statistics.mean(p for p, _ in pairs) if pairs else None,
            'positive_rate': positives / len(pairs) if pairs else None, 'calibration': calibration}


def selection(scores, rows, k):
    if type(k) is not int or k < 0:
        raise ValueError('Capacidad inválida')
    lookup = aligned(scores, rows)
    chosen = sorted(scores, key=lambda r: (-r['score'], r['application_id']))[:min(k, len(scores))]
    known = {r['application_id']: target(r) for r in rows if r.get('label_status') == 'observed'}
    chosen_known = [s for s in chosen if s['application_id'] in known]
    complete_selected = len(chosen_known) == len(chosen)
    complete_population = len(known) == len(rows)
    hits = sum(known[s['application_id']] for s in chosen_known)
    positives = sum(known.values())
    precision = hits / len(chosen) if chosen and complete_selected else None
    recall = hits / positives if complete_population and positives else None
    prevalence = positives / len(rows) if complete_population and rows else None
    lift = precision / prevalence if precision is not None and prevalence else None
    return {'eligible_count': len(rows), 'capacity_k': k, 'k_effective': len(chosen),
            'selected_ids': [s['application_id'] for s in chosen],
            'label_coverage_selected': len(chosen_known) / len(chosen) if chosen else None,
            'precision': precision, 'recall': recall, 'lift': lift,
            'population_labels_complete': complete_population}


def group_reports(scores, reference, train, rows):
    aligned(scores, rows)
    aligned(reference, rows)
    known_clients = {r['customer_id'] for r in train}
    groups = {'monthly': {}, 'customer_segments': {}}
    populations = [('monthly', month, [r for r in rows if r['scoring_at'].startswith(month)])
                   for month in sorted({r['scoring_at'][:7] for r in rows})]
    populations += [('customer_segments', name, [r for r in rows if (r['customer_id'] in known_clients) == is_known])
                    for name, is_known in [('known', True), ('new', False)]]
    for family, name, subset in populations:
        ids = {r['application_id'] for r in subset}
        subset_scores = [s for s in scores if s['application_id'] in ids]
        subset_reference = [s for s in reference if s['application_id'] in ids]
        detail = {'model': metrics(subset_scores, subset), 'reference': metrics(subset_reference, subset),
                  'unique_customers': len({r['customer_id'] for r in subset})}
        if family == 'monthly':
            detail['selection'] = selection(subset_scores, subset, POLICY['k'])
        groups[family][name] = detail
    return groups


def load_development(root):
    raw = Path(root) / 'data/raw'
    tables = {}
    for name in ['applications', 'history', 'outcomes']:
        with (raw / (name + '.csv')).open(newline='', encoding='utf-8') as stream:
            records = list(csv.DictReader(stream))
        table = {r['application_id']: r for r in records}
        if len(table) != len(records):
            raise ValueError('Clave duplicada: ' + name)
        tables[name] = table
    ids = set(tables['applications'])
    if any(set(t) != ids for t in tables.values()):
        raise ValueError('Claves no coinciden entre tablas')
    rows = []
    for identifier, app in tables['applications'].items():
        # Se decide elegibilidad ANTES de interpretar target, también para filas recientes de train.
        if app['scoring_at'] >= POLICY['validation_end_exclusive']:
            continue
        outcome = tables['outcomes'][identifier]
        if outcome['label_status'] != 'observed':
            continue
        limit = POLICY['training_cutoff'] if app['scoring_at'] < POLICY['validation_start'] else POLICY['evaluation_timestamp']
        if not outcome['label_available_at'] or outcome['label_available_at'] > limit:
            continue
        if outcome['target_30dpd_90d'] not in ['0', '1']:
            raise ValueError('Target binario inválido')
        history = tables['history'][identifier]
        if history['customer_id'] != app['customer_id']:
            raise ValueError('Cliente no coincide en join')
        row = {name: app[name] for name in POLICY['features'] if name != 'prior_late_count'}
        row.update(prior_late_count=history['prior_late_count'], history_available_at=history['available_at'],
                   application_id=identifier, customer_id=app['customer_id'], scoring_at=app['scoring_at'],
                   label_status=outcome['label_status'], label_available_at=outcome['label_available_at'],
                   target=int(outcome['target_30dpd_90d']))
        check_features(row)
        rows.append(row)
    return rows


def run(root, output, freeze_file):
    root, output = Path(root), Path(output)
    frozen = json.loads(Path(freeze_file).read_text())
    if frozen['code_sha256'] != hashlib.sha256(Path(__file__).read_bytes()).hexdigest() or frozen['policy'] != POLICY:
        raise ValueError('Código/policy difiere del freeze hash')
    expected_inputs = {'data/raw/' + name + '.csv' for name in ['applications', 'history', 'decisions', 'outcomes', 'post_decision']}
    if set(frozen['inputs']) != expected_inputs:
        raise ValueError('Freeze sin todos los inputs')
    for relative, digest in frozen['inputs'].items():
        if hashlib.sha256((root / relative).read_bytes()).hexdigest() != digest:
            raise ValueError('Input hash difiere del freeze: ' + relative)
    if output.exists():
        raise FileExistsError('Usar un output nuevo')
    rows = load_development(root)
    train = [r for r in rows if r['scoring_at'] < POLICY['training_cutoff']]
    val = [r for r in rows if POLICY['validation_start'] <= r['scoring_at'] < POLICY['validation_end_exclusive']]
    if not val:
        raise ValueError('Validation vacía')
    model = fit(train, POLICY['training_cutoff'])
    scores = predict(model, val)
    reference = [{'application_id': r['application_id'], 'score': model['reference_probability']} for r in val]
    results = {'model': metrics(scores, val), 'reference': metrics(reference, val),
               **group_reports(scores, reference, train, val)}
    summary = {'scope': 'development; solo concedidas con labels disponibles', 'training_rows': len(train),
               'validation_rows': len(val), 'reference_probability': model['reference_probability'],
               'brier_model': results['model']['brier_score'], 'brier_reference': results['reference']['brier_score'],
               'brier_improvement': results['reference']['brier_score'] - results['model']['brier_score'],
               'roc_auc_model': results['model']['roc_auc'], 'final_metrics_computed': False,
               'last_train_scoring': max(r['scoring_at'] for r in train),
               'latest_train_label_available': max(r['label_available_at'] for r in train)}
    output.mkdir(parents=True, exist_ok=False)
    for name, value in [('model', model), ('results', results), ('summary', summary), ('predictions', scores), ('reference-predictions', reference), ('execution-policy', frozen)]:
        (output / (name + '.json')).write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + '\n', encoding='utf-8')
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Baseline fijo de development; no evalúa el periodo final.')
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--freeze-file', required=True, type=Path)
    args = parser.parse_args()
    print(json.dumps(run(Path(__file__).resolve().parents[1], args.output, args.freeze_file), ensure_ascii=False, indent=2))
