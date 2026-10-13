"""Contrato mecánico; no evalúa la verdad de los hallazgos ni cambia reportes."""
import hashlib
import importlib.util
import json
from pathlib import Path

import pytest


def module():
    path = Path(__file__).parents[1] / 'scripts/evaluations/foundry_native_transport.py'
    spec = importlib.util.spec_from_file_location('report_contract_transport', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def fixture(tmp_path, condition='treatment'):
    root = tmp_path / 'workspace'
    (root / 'inputs').mkdir(parents=True)
    (root / '.runtime').mkdir()
    (root / 'reports/leakage').mkdir(parents=True)
    (root / 'case.md').write_text('Expediente público\n')
    (root / 'inputs/data.csv').write_text('x\n1\n')
    context = {'condicion': condition, 'skill': 'detect-leakage' if condition == 'treatment' else 'none',
               'version': '0.2.0' if condition == 'treatment' else None}
    (root / '.runtime/report-context.json').write_text(json.dumps(context))
    rows = '\n'.join(f'  - path: {path}\n    sha256: {hashlib.sha256((root/path).read_bytes()).hexdigest()}'
                     for path in ['case.md', 'inputs/data.csv'])
    text = f'''---
skill: {context['skill']}
version: {'"0.2.0"' if condition == 'treatment' else 'null'}
fecha: 2026-10-12
estado: auditoria_completada
condicion: {condition}
inputs:
{rows}
---

## Resumen
Auditoría del expediente; sin certificar producción.
## Hallazgos
No se ejecutó el pipeline. La correctitud requiere revisión semántica.
## Evidencia
Se identifican los inputs del expediente.
## Preguntas abiertas
¿Qué registros respaldan el proceso declarado?
## Recomendaciones
Revisar antes de aceptar decisiones.
'''
    report = root / 'reports/leakage/audit.md'
    report.write_text(text)
    return root, report, text


@pytest.mark.parametrize('condition', ['baseline', 'treatment'])
def test_valid_report_preserved_and_semantic_review_still_required(tmp_path, condition):
    root, report, text = fixture(tmp_path, condition)
    result = module().check_report_contract(root, report, 'Informe y ruta.', report_word_limit=500)
    assert result['success'] and result['errors'] == []
    assert result['semantic_review'] == 'REQUIRED'
    assert report.read_text() == text


@pytest.mark.parametrize('change,code', [
    (lambda s: s.replace('version:', 'skill_version:', 1), 'missing:version'),
    (lambda s: s.replace('version: "0.2.0"', 'version: "0.1.0"'), 'context:version'),
    (lambda s: s.replace('condicion: treatment', 'condicion: baseline'), 'context:condicion'),
    (lambda s: s.replace('## Evidencia\n', '## Otra sección\n'), 'section:Evidencia'),
    (lambda s: s.replace('sha256: ', 'sha256: f', 1), 'inputs:hash'),
    (lambda s: s.replace('## Preguntas abiertas\n', '## Preguntas abiertas\n## Preguntas abiertas\n'), 'section:Preguntas abiertas'),
    (lambda s: s.replace('estado: auditoria_completada', 'estado: null'), 'value:estado'),
    (lambda s: s.replace('fecha: 2026-10-12', 'fecha: fecha-inventada'), 'value:fecha'),
    (lambda s: s.replace('version: "0.2.0"', 'version: "0.2.0"\nversion: "0.1.0"'), 'frontmatter:duplicate'),
    (lambda s: '```markdown\n' + s + '```\n', 'frontmatter:missing'),
    (lambda s: s.replace('inputs:\n', 'inputs: []\nignored:\n'), 'inputs:coverage'),
])
def test_rejects_contract_defect_without_repairing_output(tmp_path, change, code):
    root, report, text = fixture(tmp_path)
    changed = change(text)
    report.write_text(changed)
    result = module().check_report_contract(root, report, 'Informe.', report_word_limit=500)
    assert not result['success'] and code in result['errors']
    assert report.read_text() == changed


def test_counts_whole_file_and_final_response_independently(tmp_path):
    root, report, text = fixture(tmp_path)
    total = len(text.split())
    m = module()
    assert m.check_report_contract(root, report, 'ok ' * 80, report_word_limit=total)['success']
    result = m.check_report_contract(root, report, 'ok ' * 81, report_word_limit=total - 1)
    assert result['report_words'] == total and result['final_words'] == 81
    assert {'report:word_limit', 'final:word_limit'} <= set(result['errors'])


def test_missing_report_and_final_fail_closed(tmp_path):
    root, report, _ = fixture(tmp_path)
    report.unlink()
    result = module().check_report_contract(root, report, None, report_word_limit=500)
    assert not result['success'] and 'report:missing' in result['errors']
    assert not report.exists()


def test_legacy_hash_strings_have_same_verification_without_rewriting(tmp_path):
    root, report, text = fixture(tmp_path)
    for path in ['case.md', 'inputs/data.csv']:
        value = hashlib.sha256((root/path).read_bytes()).hexdigest()
        text = text.replace(f'  - path: {path}\n    sha256: {value}', f'  - {path} sha256 {value}')
    report.write_text(text)
    result = module().check_report_contract(root, report, 'Informe.', report_word_limit=500)
    assert result['success'] and report.read_text() == text


def test_untrusted_report_path_does_not_hash_external_file(tmp_path):
    root, report, text = fixture(tmp_path)
    text = text.replace('path: inputs/data.csv', 'path: ../../private.txt')
    report.write_text(text)
    result = module().check_report_contract(root, report, 'Informe.', report_word_limit=500)
    assert not result['success'] and 'inputs:coverage' in result['errors']


@pytest.mark.parametrize('wrapper', ['```markdown\n{}\n```', '~~~markdown\n{}\n~~~', '<!--\n{}\n-->'])
def test_sections_inside_code_or_comment_do_not_satisfy_contract(tmp_path, wrapper):
    root, report, text = fixture(tmp_path)
    front, body = text.split('---', 2)[1:]
    report.write_text('---'+front+'---\n'+wrapper.format(body))
    result = module().check_report_contract(root, report, 'Informe.', report_word_limit=500)
    assert not result['success']
    assert {'section:Resumen','section:Hallazgos','section:Evidencia',
            'section:Preguntas abiertas','section:Recomendaciones'} <= set(result['errors'])


def test_valid_sections_with_a_code_example_remain_valid(tmp_path):
    root, report, text = fixture(tmp_path)
    text = text.replace('## Evidencia\n', '## Evidencia\n```python\n## Resumen\n# <!-- literal de código\n```\n')
    report.write_text(text)
    assert module().check_report_contract(root, report, 'Informe.', report_word_limit=500)['success']


def test_bad_yaml_date_is_not_misreported_as_duplicate_key(tmp_path):
    root, report, text = fixture(tmp_path)
    report.write_text(text.replace('fecha: 2026-10-12', 'fecha: 2026-99-99'))
    result = module().check_report_contract(root, report, 'Informe.', report_word_limit=500)
    assert not result['success'] and 'frontmatter:invalid' in result['errors']
    assert 'frontmatter:duplicate' not in result['errors']


def test_corrupt_runtime_context_is_a_preserved_contract_failure(tmp_path):
    root, report, text = fixture(tmp_path)
    (root/'.runtime/report-context.json').write_text('invalid-json')
    result = module().check_report_contract(root, report, 'Informe.', report_word_limit=500)
    assert not result['success'] and 'contract:unreadable' in result['errors']
    assert report.read_text() == text


def test_input_symlink_is_rejected_before_hashing_external_bytes(tmp_path,monkeypatch):
    root, report, _ = fixture(tmp_path)
    external=tmp_path/'private.txt';external.write_text('No autorizado')
    data=root/'inputs/data.csv';data.unlink();data.symlink_to(external)
    m=module();original=m.digest;hashed=[]
    def observed_digest(path):
        hashed.append(Path(path).resolve())
        return original(path)
    monkeypatch.setattr(m,'digest',observed_digest)
    result=m.check_report_contract(root,report,'Informe.',report_word_limit=500)
    assert not result['success'] and 'inputs:unsafe' in result['errors']
    assert external not in hashed
