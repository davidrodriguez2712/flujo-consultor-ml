"""Coordinación local sin credenciales ni llamadas reales."""
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace
import pytest


def module():
    path=Path(__file__).parents[1]/'scripts/evaluations/foundry_study.py'
    spec=importlib.util.spec_from_file_location('study',path)
    m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m


@pytest.mark.parametrize('approval',[{}, {'status':'APPROVED','total_budget_usd':.1},
    {'status':'APPROVED','total_budget_usd':.11,'package_accepted':True,'execution_manifest_sha256':'hash'},
    {'status':'APPROVED','total_budget_usd':True,'package_accepted':True,'execution_manifest_sha256':'hash'},
    {'status':'APPROVED','total_budget_usd':.1,'package_accepted':False,'execution_manifest_sha256':'hash'}])
def test_authorization_fail_closed(approval):
    with pytest.raises(ValueError):module().require_approval(approval,'hash')


def test_authorization_exact_package():
    assert module().require_approval({'status':'APPROVED','total_budget_usd':.1,'package_accepted':True,'execution_manifest_sha256':'hash'},'hash')==.1


@pytest.mark.parametrize('failure',[None,2])
def test_schedule_shared_workflow_and_stop(tmp_path,failure):
    m=module();calls=[]
    proxy=SimpleNamespace(budget=SimpleNamespace(entries=[],max_requests=56),rejections=[])
    def invoke(case,out,proxy,cli,**kw):
        calls.append((case.name,kw));proxy.budget.entries.append({'estimated_usd':.001})
        return {'runtime_success':len(calls)!=failure}
    result=m.execute(tmp_path/'package',tmp_path/'out',proxy,'fake',SimpleNamespace(invoke=invoke))
    assert len(calls)==(7 if failure is None else 2)
    assert result['effectiveness']=='NOT_REVIEWED'
    assert result['status']==('COMPLETED_PENDING_CONTENT_REVIEW' if failure is None else 'STOPPED_RUNTIME_FAILURE')
    assert all(x[1]['workflow']==tmp_path/'package/workflow.md' for x in calls)
    if failure is None:
        assert [bool(x[1]['skill']) for x in calls]==[False,False,True,True,False,False,True]
    assert json.loads((tmp_path/'out/ledger.json').read_text())['entries']==proxy.budget.entries
    assert proxy.budget.max_requests==len(calls)
    with pytest.raises(FileExistsError):m.execute(tmp_path/'package',tmp_path/'out',proxy,'fake',SimpleNamespace(invoke=invoke))


def test_exception_preserves_ledger_and_stops(tmp_path):
    m=module();proxy=SimpleNamespace(budget=SimpleNamespace(entries=[],max_requests=56),rejections=[])
    def invoke(*a,**kw):
        proxy.budget.entries.append({'estimated_usd':None,'reserved_usd':.05});raise OSError('simulated')
    with pytest.raises(OSError):m.execute(tmp_path/'p',tmp_path/'out',proxy,'fake',SimpleNamespace(invoke=invoke))
    assert proxy.budget.max_requests==1
    assert json.loads((tmp_path/'out/summary.json').read_text())['status']=='STOPPED_COORDINATOR_FAILURE'
