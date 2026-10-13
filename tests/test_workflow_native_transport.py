"""Transporte nativo probado sin CLI real ni proveedor."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest


def module():
    spec = importlib.util.spec_from_file_location('workflow_native_transport', Path(__file__).parents[1]/'scripts/evaluations/workflow_native_transport.py')
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_budget_authorization_rejects_missing_or_unbound_approval():
    # Rompe si una aprobación genérica o el dólar de Windows habilita esta ronda.
    m=module()
    for approval in ({}, {'status':'APPROVED','total_budget_usd':1},
                     {'status':'APPROVED','total_budget_usd':0.2,'execution_manifest_sha256':'other'}):
        with pytest.raises(ValueError):m.require_approval(approval,'frozen-hash')
    assert m.require_approval({'status':'APPROVED','total_budget_usd':0.2,
        'execution_manifest_sha256':'frozen-hash'},'frozen-hash') == 0.2


def test_native_transport_preserves_text_and_stops_after_one_request(tmp_path,monkeypatch):
    # Rompe si añade expected al prompt, reutiliza cwd o admite requests adicionales.
    m=module()
    ledger=SimpleNamespace(entries=[],max_requests=13)
    proxy=SimpleNamespace(url='http://127.0.0.1:1234',budget=ledger,key='secret-test')
    def native(argv, **kwargs):
        assert kwargs['input']=='expediente público'
        assert Path(kwargs['cwd']).is_dir() and not list(Path(kwargs['cwd']).iterdir())
        assert kwargs['env']['ANTHROPIC_API_KEY']=='local-proxy-placeholder'
        assert kwargs['env']['ANTHROPIC_BASE_URL']==proxy.url
        assert '--json-schema' not in argv
        assert argv[argv.index('--tools')+1]==''
        assert ledger.max_requests==1
        ledger.entries.append({'estimated_usd':0.001})
        return SimpleNamespace(returncode=0,stdout=json.dumps({'type':'result','subtype':'success',
            'is_error':False,'result':'{"status":"READY"}',
            'modelUsage':{'claude-haiku-5-5':{'inputTokens':2,'outputTokens':3}}}),stderr='')
    monkeypatch.setattr(m.subprocess,'run',native)
    out=tmp_path/'one'
    result=m.invoke('expediente público',out,proxy,'/native/claude')
    assert result['runtime_success'] is True
    assert (out/'result.txt').read_text()=='{"status":"READY"}'
    assert not Path(result['temporary_cwd']).exists()
    assert ledger.max_requests==1
    with pytest.raises(FileExistsError):m.invoke('expediente público',out,proxy,'/native/claude')


def test_native_transport_keeps_malformed_output_without_repair(tmp_path,monkeypatch):
    m=module()
    ledger=SimpleNamespace(entries=[],max_requests=13)
    proxy=SimpleNamespace(url='http://127.0.0.1:1234',budget=ledger,key='secret-test')
    def native(*args,**kwargs):
        ledger.entries.append({'estimated_usd':None})
        return SimpleNamespace(returncode=0,stdout='not-json',stderr='secret-test')
    monkeypatch.setattr(m.subprocess,'run',native)
    result=m.invoke('public',tmp_path/'broken',proxy,'/native/claude')
    assert result['runtime_success'] is False
    assert result['usage_known'] is False
    assert (tmp_path/'broken/stdout.txt').read_text()=='not-json'
    assert (tmp_path/'broken/stderr.txt').read_text()=='[REDACTED]'
    assert not (tmp_path/'broken/result.txt').exists()


def test_transfer_system_prompt_is_explicit_and_preserves_markdown(tmp_path,monkeypatch):
    # Rompe si fuerza JSON en transferencia o interpreta/repara el texto del modelo.
    m=module()
    ledger=SimpleNamespace(entries=[],max_requests=13)
    proxy=SimpleNamespace(url='http://127.0.0.1:1234',budget=ledger,key='secret-test')
    memo='## Estado\nREADY\n'
    def native(argv,**kwargs):
        assert argv[argv.index('--system-prompt')+1]==m.TRANSFER_SYSTEM
        assert argv[argv.index('--output-format')+1]=='json'
        assert '--json-schema' not in argv and kwargs['input']=='público Markdown'
        ledger.entries.append({'estimated_usd':0.001})
        return SimpleNamespace(returncode=0,stdout=json.dumps({'type':'result','subtype':'success',
            'is_error':False,'result':memo,'modelUsage':{m.MODEL:{'inputTokens':2,'outputTokens':3}}}),stderr='')
    monkeypatch.setattr(m.subprocess,'run',native)
    result=m.invoke('público Markdown',tmp_path/'memo',proxy,'/native/claude',system_prompt=m.TRANSFER_SYSTEM)
    assert result['runtime_success'] is True
    assert (tmp_path/'memo/result.txt').read_text()==memo
    assert ledger.max_requests==1
