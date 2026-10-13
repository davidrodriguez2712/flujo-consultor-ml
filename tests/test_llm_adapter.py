import sys
from acos.llm_adapter import llm_proposal
from acos.contracts import ProjectProfile


def profile():return ProjectProfile(project={'slug':'a','name':'A'},engagement={'decision':'Conservar decisión'})


def test_llm_no_consent_no_subprocess(tmp_path):
    marker=tmp_path/'marker'
    assert llm_proposal(profile(),[sys.executable,'-c',f'open({str(marker)!r},"w").write("bad")'],lambda payload:False) is None
    assert not marker.exists()


def test_llm_invalid_or_timeout_falls_back():
    assert llm_proposal(profile(),[sys.executable,'-c','print("not json")'],lambda payload:True) is None


def test_llm_cannot_change_business_facts():
    p=profile()
    assert llm_proposal(p,[sys.executable,'-c','print(\'{"archetypes":["OPTIMIZE"],"reasons":["capacidad"],"unresolved":[],"decision":"inventada"}\')'],lambda payload:True) is None
    result=llm_proposal(p,[sys.executable,'-c','print(\'{"archetypes":["OPTIMIZE"],"reasons":["capacidad"],"unresolved":[]}\')'],lambda payload:True)
    assert result.archetypes==['OPTIMIZE'] and p.engagement.decision=='Conservar decisión'


def test_llm_timeout_returns_to_local(monkeypatch):
    import acos.llm_adapter as adapter
    run=adapter.subprocess.run
    def short_timeout(*args,**kwargs):
        kwargs['timeout']=0.02
        return run(*args,**kwargs)
    monkeypatch.setattr(adapter.subprocess,'run',short_timeout)
    assert llm_proposal(profile(),[sys.executable,'-c','import time; time.sleep(0.2)'],lambda payload:True) is None
