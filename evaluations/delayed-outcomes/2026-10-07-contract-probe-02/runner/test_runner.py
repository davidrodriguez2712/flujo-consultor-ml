"""Pruebas locales de registro; no llamadas a servicios."""
import importlib.util
import json
from pathlib import Path
import sys

SCRIPT=Path(__file__).with_name('run.py')
def module():
    assert SCRIPT.is_file(), 'Falta runner aprobado'
    spec=importlib.util.spec_from_file_location('probe_runner',SCRIPT)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def fixtures(root):
    (root/'guidance').mkdir();(root/'cases').mkdir()
    (root/'task.md').write_text('Tarea común')
    (root/'guidance/baseline-design-validation-0.1.0.md').write_text('Pauta actual')
    (root/'guidance/temporal-contract-0.1.0.md').write_text('Contrato adicional')
    for case in 'ABCDEF':
        p=root/'cases'/case;p.mkdir();(p/'case.md').write_text('Caso '+case)
        (p/'inputs.json').write_text('{"id":"'+case+'"}')
        (p/'expected.json').write_text('SECRETO_EXPECTED_NO_ENVIAR')

def test_prepare_keeps_expected_private_and_twenty_four_calls(tmp_path):
    fixtures(tmp_path);m=module();plan=m.prepare(tmp_path)
    assert len(plan)==24 and len({(r['case'],r['branch'],r['repetition']) for r in plan})==24
    a=(tmp_path/'payloads/A/baseline.txt').read_text();b=(tmp_path/'payloads/A/treatment.txt').read_text()
    assert b.startswith(a) and 'Contrato adicional' in b
    assert 'SECRETO_EXPECTED_NO_ENVIAR' not in a+b
    assert [(p['branch'],p['repetition']) for p in plan if p['case']=='A']==[('baseline',1),('treatment',1),('treatment',2),('baseline',2)]

def test_call_preserves_payload_and_raw_and_metadata(tmp_path):
    fixtures(tmp_path);m=module();m.prepare(tmp_path)
    cli=tmp_path/'stub.py';cli.write_text('import json,sys\np=sys.stdin.read()\nprint(json.dumps({"result":"{}","session_id":"stub-session","is_error":False,"modelUsage":{}}))\n')
    record=m.run_one(tmp_path,'A','baseline',1,[sys.executable,str(cli)],'stub-model','stub-version')
    p=tmp_path/'runs/A/baseline/1'
    assert record['runtime_ok'] and record['exit_code']==0
    assert (p/'payload.txt').read_bytes()==(tmp_path/'payloads/A/baseline.txt').read_bytes()
    assert json.loads((p/'raw.json').read_text())['result']==(p/'result.txt').read_text()
    metadata=json.loads((p/'metadata.json').read_text())
    assert metadata['cwd']!=str(tmp_path) and metadata['request_sha256']
    assert metadata['effective_configuration']['effort']=='unknown'

def test_failed_process_is_archived_and_not_counted_valid(tmp_path):
    fixtures(tmp_path);m=module();m.prepare(tmp_path)
    cli=tmp_path/'failure.py';cli.write_text('import sys\nprint("fallo",file=sys.stderr)\nsys.exit(7)\n')
    record=m.run_one(tmp_path,'A','baseline',1,[sys.executable,str(cli)],'stub-model','stub-version')
    assert record['exit_code']==7 and not record['runtime_ok']
    assert 'fallo' in (tmp_path/'runs/A/baseline/1/stderr.txt').read_text()


def test_resume_does_not_skip_previous_wrong_model(tmp_path,monkeypatch):
    import subprocess
    import pytest
    fixtures(tmp_path);m=module();m.prepare(tmp_path)
    version=subprocess.run([sys.executable,'--version'],capture_output=True,text=True,check=True).stdout.strip()
    m.freeze(tmp_path,version)
    p=tmp_path/'runs/A/baseline/1';p.mkdir(parents=True)
    (p/'metadata.json').write_text(json.dumps({'runtime_ok':True,'model_usage':{'wrong-model':{}},'cli_version':version}))
    monkeypatch.setattr(m,'__file__',str(tmp_path/'runner/run.py'))
    monkeypatch.setattr(m.shutil,'which',lambda _:sys.executable)
    monkeypatch.setattr(sys,'argv',['run.py','--run'])
    with pytest.raises(ValueError,match='Modelo'):m.main()


def test_malformed_model_usage_still_gets_failure_metadata(tmp_path):
    fixtures(tmp_path);m=module();m.prepare(tmp_path)
    cli=tmp_path/'malformed.py';cli.write_text('import json\nprint(json.dumps({"result":"{}","is_error":False,"modelUsage":None}))\n')
    record=m.run_one(tmp_path,'A','baseline',1,[sys.executable,str(cli)],'stub-model','stub-version')
    assert not record['runtime_ok']
    assert record['model_usage']=={} and record['model_usage_reported'] is None
    assert (tmp_path/'runs/A/baseline/1/metadata.json').is_file()
