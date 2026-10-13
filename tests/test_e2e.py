from pathlib import Path
import shutil
import socket
import pytest
from acos.contracts import ProjectProfile
from acos.yaml_io import read_yaml
from acos.catalog import load_catalog
from acos.foundry import scan_foundry
from acos.resolver import resolve,confirm_plan
from acos.compiler import compile_project
from acos.project import load_project,next_objective
from acos.gates import validate_gate

FIXTURES=Path(__file__).parent/'fixtures/profiles'

@pytest.mark.parametrize('name,needed,absent',[
    ('fraud',{'data_analysis','supervised_model','selection','optimization'}, {'genai_solution','software_ui'}),
    ('research',{'research','executive_delivery'}, {'data_analysis','supervised_model'}),
    ('clv',{'supervised_model','optimization','business_case'},{'intervention'}),
    ('uplift',{'intervention','selection','optimization'},{'supervised_model'}),
    ('unlabeled-anomaly',{'data_analysis','selection'},{'supervised_model','intervention'}),
    ('ui-handoff',{'software_ui','recommendation'},{'genai_solution'}),
    ('inherited-model',{'supervised_model','data_analysis'},{'software_ui'})])
def test_seven_profiles_compile_only_selected_modules(tmp_path,name,needed,absent):
    profile=ProjectProfile.model_validate(read_yaml(FIXTURES/(name+'.yaml')))
    plan=resolve(profile,load_catalog(),scan_foundry(None))
    assert needed<=set(plan.selection.modules) and not absent & set(plan.selection.modules)
    target=tmp_path/name;compile_project(confirm_plan(plan,True),target,False)
    result=validate_gate(load_project(target))
    assert result.status in ('BLOCKED','NEEDS_REVIEW')
    assert next_objective(load_project(target))['stage']==profile.engagement.current_stage


def test_moved_workspace_runs_without_foundry(tmp_path,foundry):
    from conftest import make_skill
    make_skill(foundry)
    p=ProjectProfile.model_validate(read_yaml(FIXTURES/'fraud.yaml'))
    plan=resolve(p,load_catalog(),scan_foundry(foundry))
    compile_project(confirm_plan(plan,True),tmp_path/'first',False)
    shutil.move(tmp_path/'first',tmp_path/'moved');shutil.rmtree(foundry)
    assert next_objective(load_project(tmp_path/'moved'))['stage']=='framing'


def test_reproducible_plan_from_confirmed_profile():
    p=ProjectProfile.model_validate(read_yaml(FIXTURES/'uplift.yaml'))
    assert resolve(p,load_catalog(),scan_foundry(None)).selection==resolve(p,load_catalog(),scan_foundry(None)).selection


def test_no_network_in_local_path(tmp_path,monkeypatch):
    def forbid(*args,**kwargs):raise AssertionError('Network forbidden')
    monkeypatch.setattr(socket,'create_connection',forbid)
    p=ProjectProfile.model_validate(read_yaml(FIXTURES/'research.yaml'))
    compile_project(confirm_plan(resolve(p,load_catalog(),scan_foundry(None)),True),tmp_path/'local',False)
    assert (tmp_path/'local/MANUAL.md').is_file()


def test_runtime_skill_paths_match_selection(tmp_path,foundry):
    from conftest import make_skill
    make_skill(foundry)
    p=ProjectProfile.model_validate(read_yaml(FIXTURES/'fraud.yaml'));p.runtimes=['codex']
    manifest=compile_project(confirm_plan(resolve(p,load_catalog(),scan_foundry(foundry)),True),tmp_path/'p',False)
    assert manifest.skills[0]['runtime_paths']==['.agents/skills/understand-dataset']
    assert not (tmp_path/'p/.claude').exists()
