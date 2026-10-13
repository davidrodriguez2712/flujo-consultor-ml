"""Regresiones del checker local, con expected literal independiente."""
import importlib.util
import json
from pathlib import Path
import pytest

CHECKER=Path(__file__).with_name('check.py')
EXPECTED={'X':{'outcome_state_at_extraction':'observed_negative','label_availability_at_training':'available','train_eligibility':'eligible'}}

def evaluate(text):
    assert CHECKER.is_file(), 'Falta el checker aprobado para la ronda'
    spec=importlib.util.spec_from_file_location('temporal_probe_checker',CHECKER)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module.evaluate(text,EXPECTED)

def payload():
    return {'rows':[{'id':'X',**EXPECTED['X'],'reason':'Según fechas y certificación provistas.'}], 'open_questions':[], 'gate_decision':'NEEDS_REVIEW'}

def test_plain_json_and_correct_decisions():
    result=evaluate(json.dumps(payload()))
    assert result['strict_format_pass'] and result['payload_schema_pass'] and result['content_evaluable']
    assert result['field_matches']==3 and result['eligible_false_positives']==0


def test_fences_remain_format_failure_despite_diagnostic_accuracy():
    result=evaluate('```json\n'+json.dumps(payload())+'\n```')
    assert not result['strict_format_pass'] and result['diagnostic_parse_used']
    assert result['field_matches']==3


def test_excluding_valid_row_is_recorded():
    data=payload();data['rows'][0]['train_eligibility']='exclude'
    result=evaluate(json.dumps(data))
    assert result['field_matches']==2 and result['valid_rows_excluded']==1


def test_duplicate_ids_are_not_double_counted():
    data=payload();data['rows'].append(data['rows'][0].copy())
    result=evaluate(json.dumps(data))
    assert not result['payload_schema_pass'] and not result['ids_exact']
    assert result['field_matches']==0


@pytest.mark.parametrize('text',['{"rows": [], "x": NaN}', '{"rows": [], "rows": []}', 'prefacio {"rows":[]}'])
def test_invalid_json_is_not_accepted(text):
    result=evaluate(text)
    assert not result['strict_format_pass'] and not result['payload_schema_pass'] and not result['content_evaluable']


def test_missing_reason_fails_schema():
    data=payload();data['rows'][0]['reason']=''
    assert not evaluate(json.dumps(data))['payload_schema_pass']
