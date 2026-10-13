import importlib.util
from pathlib import Path
import pytest


def module():
    path=Path(__file__).parents[1]/'scripts/evaluations/workflow_output_checker.py'
    spec=importlib.util.spec_from_file_location('workflow_output_checker',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


def valid(status='READY'):
    return {'status':status,'findings':[{'statement':'La fila citada corresponde al resultado.','evidence_paths':['analysis/source.json']}],'proposed_actions':['Preparar siguiente tarea.'],'next_step':'Revisar con owner.','limitations':['Fixture hipotético.']}


def test_json_format_is_not_semantic_approval():
    import json
    result=module().check_text(json.dumps(valid()),{'status':'READY'},['analysis/source.json'])
    assert result['strict_json_pass'] and result['schema_pass'] and result['status_matches']
    assert result['references_exist']
    assert result['semantic_review']=='NOT_RUN'
    assert result['overall_content_pass'] is None


@pytest.mark.parametrize('text',['```json\n{}\n```','{"status":"READY","status":"READY"}','{"value":NaN}','{"value":1e999}'])
def test_invalid_strict_json_is_preserved_as_failure(text):
    result=module().check_text(text,{'status':'READY'},[])
    assert result['strict_json_pass'] is False
    assert result['status_matches'] is None


def test_unknown_reference_and_wrong_status_are_separate():
    import json
    result=module().check_text(json.dumps(valid('MUST_CORRECT')),{'status':'READY'},[])
    assert result['schema_pass']
    assert result['status_matches'] is False
    assert result['references_exist'] is False
    assert result['unknown_references']==['analysis/source.json']


def test_types_and_required_fields_are_checked():
    import json
    obj=valid();obj['findings']='not a list'
    result=module().check_text(json.dumps(obj),{'status':'READY'},[])
    assert result['strict_json_pass'] and result['schema_pass'] is False


def test_valid_output_may_include_extra_fields_not_forbidden_by_frozen_contract():
    import json
    obj=valid();obj['note']='Campo adicional, sin cambiar campos requeridos.'
    assert module().check_text(json.dumps(obj),{'status':'READY'},['analysis/source.json'])['schema_pass']
