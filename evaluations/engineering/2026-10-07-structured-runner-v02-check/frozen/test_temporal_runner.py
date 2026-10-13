"""Runner v0.2: salida nativa y archivo completo de errores, sin servicios."""
import importlib.util
import json
from pathlib import Path
import sys
import pytest

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'scripts/evaluations/temporal_runner.py'

def runner():
    assert SCRIPT.is_file(), 'Falta el runner versionado aprobado'
    spec=importlib.util.spec_from_file_location('temporal_runner_v02',SCRIPT)
    m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
    return m

def payload():
    return {'rows':[{'id':'X','outcome_state_at_extraction':'pending','label_availability_at_training':'unavailable','train_eligibility':'exclude','reason':'La certificación es posterior al entrenamiento.'}], 'open_questions':[], 'gate_decision':'NEEDS_REVIEW'}

def envelope(structured=True):
    raw={'type':'result','subtype':'success','is_error':False,'result':'','session_id':'stub-session','modelUsage':{'stub-model':{}},'total_cost_usd':0}
    if structured:raw['structured_output']=payload()
    return raw

def invoke(tmp_path,raw,code=0):
    m=runner();inp=tmp_path/'input.txt';inp.write_text('Reglas y datos sintéticos; sin expected.')
    cli=tmp_path/'cli.py'
    cli.write_text('import sys\nif "--version" in sys.argv:\n print("stub-cli 1.0")\nelse:\n sys.stdin.read()\n print('+repr(json.dumps(raw))+')\n sys.exit('+str(code)+')\n')
    out=tmp_path/'output'
    result=m.run_one(inp,out,[sys.executable,str(cli)],'stub-model')
    return result,out

def test_empty_result_with_structured_object_is_valid(tmp_path):
    metadata,out=invoke(tmp_path,envelope())
    assert metadata['runtime_success'] and metadata['schema_conformant'] and metadata['model_matches']
    assert metadata['content_validation']=='NOT_RUN'
    assert json.loads((out/'structured-output.json').read_text())==payload()
    assert (out/'result.txt').read_text()==''
    raw=json.loads((out/'raw.json').read_text())
    assert raw==envelope()
    request=json.loads((out/'request.json').read_text());argv=request['argv']
    assert json.loads(argv[argv.index('--json-schema')+1])==runner().schema_document()


def test_valid_result_text_does_not_replace_missing_structured_output(tmp_path):
    raw=envelope(False);raw['result']=json.dumps(payload())
    metadata,out=invoke(tmp_path,raw)
    assert metadata['runtime_success'] and not metadata['schema_conformant']
    assert any(f['code']=='structured-missing' for f in metadata['findings'])
    assert not (out/'structured-output.json').exists()


@pytest.mark.parametrize('defect',['missing_reason','duplicate_id','empty_question'])
def test_invalid_structured_object_is_preserved_and_blocked(tmp_path,defect):
    raw=envelope()
    if defect=='missing_reason':raw['structured_output']['rows'][0].pop('reason')
    if defect=='duplicate_id':raw['structured_output']['rows'].append(raw['structured_output']['rows'][0].copy())
    if defect=='empty_question':raw['structured_output']['open_questions']=[' ']
    metadata,out=invoke(tmp_path,raw)
    assert metadata['runtime_success'] and not metadata['schema_conformant']
    assert json.loads((out/'structured-output.json').read_text())==raw['structured_output']
    assert (out/'metadata.json').is_file()


def test_schema_does_not_force_correct_decision_or_human_approval(tmp_path):
    raw=envelope();raw['structured_output']['rows'][0]['train_eligibility']='eligible'
    raw['structured_output']['gate_decision']='PASS'
    metadata,out=invoke(tmp_path,raw)
    assert metadata['schema_conformant'] and metadata['content_validation']=='NOT_RUN'
    checker=ROOT/'evaluations/delayed-outcomes/2026-10-07-contract-probe-02/checker/check.py'
    spec=importlib.util.spec_from_file_location('original_checker',checker);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
    expected={'X':{'outcome_state_at_extraction':'pending','label_availability_at_training':'unavailable','train_eligibility':'exclude'}}
    result=m.evaluate((out/'structured-output.json').read_text(),expected)
    assert result['eligible_false_positives']==1 and not result['gate_matches']


def test_runtime_failure_is_separate_from_valid_schema(tmp_path):
    metadata,out=invoke(tmp_path,envelope(),7)
    assert not metadata['runtime_success'] and metadata['schema_conformant']
    assert metadata['exit_code']==7 and (out/'raw.json').is_file()


def test_malformed_model_usage_gets_metadata(tmp_path):
    raw=envelope();raw['modelUsage']=None
    metadata,out=invoke(tmp_path,raw)
    assert metadata['runtime_success'] and not metadata['model_matches']
    assert metadata['model_usage_reported'] is None and (out/'metadata.json').is_file()


def test_wrong_model_is_not_hidden(tmp_path):
    raw=envelope();raw['modelUsage']={'different-model':{}}
    metadata,_=invoke(tmp_path,raw)
    assert metadata['runtime_success'] and not metadata['model_matches']


def test_existing_destination_preserves_files(tmp_path):
    m=runner();inp=tmp_path/'input.txt';inp.write_text('Datos');out=tmp_path/'existing';out.mkdir();(out/'mine').write_text('original')
    with pytest.raises(FileExistsError):m.run_one(inp,out,[sys.executable],'stub-model')
    assert sorted(p.name for p in out.iterdir())==['mine'] and (out/'mine').read_text()=='original'


def test_cli_receives_supported_schema_dialect(tmp_path):
    m=runner();inp=tmp_path/'input.txt';inp.write_text('Auditoría ficticia')
    raw=json.dumps(envelope())
    cli=tmp_path/'draft7_cli.py'
    cli.write_text('import json,sys\nif "--version" in sys.argv:\n print("stub-cli 1.0")\nelse:\n schema=json.loads(sys.argv[sys.argv.index("--json-schema")+1])\n if schema.get("$schema")!="http://json-schema.org/draft-07/schema#":\n  print("unsupported schema dialect",file=sys.stderr)\n  sys.exit(2)\n print('+repr(raw)+')\n')
    result=m.run_one(inp,tmp_path/'output',[sys.executable,str(cli)],'stub-model')
    assert result['runtime_success'] and result['schema_conformant']


@pytest.mark.parametrize('field',['id','reason','question'])
def test_invalid_unicode_is_archived_and_fails_local_validation(tmp_path,field):
    raw=envelope()
    if field=='question':raw['structured_output']['open_questions']=['\ud800']
    else:raw['structured_output']['rows'][0][field]='\ud800'
    metadata,out=invoke(tmp_path,raw)
    assert metadata['runtime_success'] and not metadata['schema_conformant']
    assert json.loads((out/'structured-output.json').read_text())==raw['structured_output']
    assert json.loads((out/'metadata.json').read_text())['schema_conformant'] is False


def test_invalid_unicode_in_optional_text_does_not_erase_metadata(tmp_path):
    raw=envelope();raw['result']='\ud800'
    metadata,out=invoke(tmp_path,raw)
    assert metadata['schema_conformant'] and (out/'metadata.json').is_file()
    assert not (out/'result.txt').exists()
    assert json.loads((out/'result-escaped.json').read_text())==raw['result']
    assert any(f['code']=='result-unicode-invalid' for f in metadata['findings'])
