"""Contrato de transferencia; no prueba eficacia semántica de agentes."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import pytest

SCRIPT=Path(__file__).parents[1]/'scripts/evaluations/workflow_transfer_checker.py'
MEMO='''## Estado
READY

## Hallazgos
Escenario documentado en `analysis/scenario.json` y [borrador](drafts/pricing.md).

## Acciones propuestas
Revisar sensibilidad.

## Siguiente paso
Revisar con owner.

## Límites
Simulación, no evidencia causal.
'''
PATHS=['analysis/scenario.json','drafts/pricing.md']

def module():
    assert SCRIPT.exists(), 'Falta checker de transferencia JSON/Markdown'
    spec=importlib.util.spec_from_file_location('workflow_transfer_checker',SCRIPT)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def test_markdown_format_does_not_imply_content_approval():
    # Rompe si solo valida JSON o convierte estructura en aceptación semántica.
    result=module().check_text(MEMO,{'status':'READY','format':'markdown'},PATHS)
    assert result['format_pass'] is True and result['status_matches'] is True
    assert result['references_exist'] is True
    assert result['referenced_paths']==sorted(PATHS)
    assert result['semantic_review']=='NOT_RUN' and result['overall_content_pass'] is None


@pytest.mark.parametrize('bad',[
    'Prefacio\n'+MEMO, '```markdown\n'+MEMO+'```',
    MEMO.replace('## Estado','## Otro'),
    MEMO.replace('## Límites','### Límites'),
    MEMO+'\n## Extra\nTexto.',
    MEMO.replace('READY','READY\nMUST_CORRECT'),
    MEMO.replace('READY','APROBADO'),
    MEMO.replace('Simulación, no evidencia causal.',''),
    json.dumps({'status':'READY'}),
])
def test_markdown_rejects_wrong_structure_without_repair(bad):
    result=module().check_text(bad,{'status':'READY','format':'markdown'},PATHS)
    assert result['format_pass'] is False
    assert result['overall_content_pass'] is None


def test_markdown_keeps_wrong_status_and_unknown_paths_separate():
    memo=MEMO.replace('READY','MUST_CORRECT').replace('drafts/pricing.md','drafts/unknown.md')
    result=module().check_text(memo,{'status':'READY','format':'markdown'},PATHS)
    assert result['format_pass'] is True
    assert result['status_matches'] is False and result['references_exist'] is False
    assert result['unknown_references']==['drafts/unknown.md']


def test_markdown_accepts_emphasis_plain_paths_and_ignores_inner_code_headings():
    memo=MEMO.replace('READY','**READY**').replace('`analysis/scenario.json`','analysis/scenario.json')
    memo=memo.replace('Revisar sensibilidad.','Revisar sensibilidad.\n\n```text\n## No es una sección\n```')
    result=module().check_text(memo,{'status':'READY','format':'markdown'},PATHS)
    assert result['format_pass'] is True and result['references_exist'] is True
    assert result['referenced_paths']==sorted(PATHS)


def test_missing_references_is_not_support_proof():
    result=module().check_text(MEMO.replace('Escenario documentado en `analysis/scenario.json` y [borrador](drafts/pricing.md).','Escenario documentado.'),{'status':'READY','format':'markdown'},PATHS)
    assert result['format_pass'] is True
    assert result['references_exist'] is True and result['references_present'] is False
    assert result['overall_content_pass'] is None


def test_json_reuses_strict_checker_without_repair():
    m=module();expected={'status':'READY','format':'json'}
    obj={'status':'READY','findings':[],'proposed_actions':[],'next_step':'Revisar','limitations':[]}
    assert m.check_text(json.dumps(obj),expected,[])['format_pass'] is True
    fenced=m.check_text('```json\n'+json.dumps(obj)+'\n```',expected,[])
    assert fenced['format_pass'] is False and fenced['strict_json_pass'] is False
    assert m.check_text('{"status":"READY","status":"READY"}',expected,[])['format_pass'] is False


def test_unknown_format_fails_closed():
    with pytest.raises(ValueError):module().check_text(MEMO,{'status':'READY','format':'html'},PATHS)


def test_transfer_checker_cli_preserves_file_and_returns_failure(tmp_path):
    module()
    raw=tmp_path/'raw.txt';raw.write_text('Prefacio\n'+MEMO)
    expected=tmp_path/'expected.json';expected.write_text(json.dumps({'status':'READY','format':'markdown'}))
    artifacts=tmp_path/'artifacts.json';artifacts.write_text(json.dumps(dict.fromkeys(PATHS,'')))
    before=raw.read_bytes()
    result=subprocess.run([sys.executable,str(SCRIPT),str(raw),str(expected),str(artifacts)],capture_output=True,text=True)
    assert result.returncode==4 and json.loads(result.stdout)['format_pass'] is False
    assert raw.read_bytes()==before
