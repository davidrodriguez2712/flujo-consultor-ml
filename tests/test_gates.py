from acos.gates import validate_gate
from acos.project import load_project
from acos.compiler import compile_project
from acos.yaml_io import read_yaml,write_yaml_bytes
from test_compiler import plan


def test_existing_output_does_not_pass_gate(tmp_path):
    compile_project(plan(),tmp_path,True)
    assert validate_gate(load_project(tmp_path)).status=='NEEDS_REVIEW'


def review(tmp_path,**kwargs):
    p=tmp_path/'.acos/state.yaml';s=read_yaml(p)
    from acos.contracts import ProjectProfile,canonical_sha256
    profile=ProjectProfile.model_validate(read_yaml(tmp_path/'.acos/project-profile.yaml'))
    s['gate_reviews']={'discovery':{'decision':'PASS','reviewer':'David','evidence':['context/business_context.md'],'profile_sha256':canonical_sha256(profile),**kwargs}}
    p.write_bytes(write_yaml_bytes(s))


def test_human_review_requires_reviewer_and_evidence(tmp_path):
    compile_project(plan(),tmp_path,True);review(tmp_path,reviewer='',evidence=[])
    assert validate_gate(load_project(tmp_path)).status=='NEEDS_REVIEW'
    review(tmp_path)
    assert validate_gate(load_project(tmp_path)).status=='PASS'


def test_profile_drift_blocks_gate(tmp_path):
    compile_project(plan(),tmp_path,True)
    p=tmp_path/'.acos/project-profile.yaml';s=read_yaml(p);s['project']['name']='Changed';p.write_bytes(write_yaml_bytes(s))
    assert validate_gate(load_project(tmp_path)).status=='BLOCKED'


def test_invalid_stage_sequence_reports_block(tmp_path):
    compile_project(plan(),tmp_path,True)
    p=tmp_path/'.acos/state.yaml';s=read_yaml(p);s['current_stage']='delivery';p.write_bytes(write_yaml_bytes(s))
    assert validate_gate(load_project(tmp_path)).status=='BLOCKED'


def test_skill_snapshot_tampering_blocks_gate(foundry,tmp_path):
    from conftest import make_skill
    make_skill(foundry);target=tmp_path/'project';compile_project(plan(foundry),target,False)
    (target/'.agents/skills/understand-dataset/SKILL.md').write_text('tampered')
    assert validate_gate(load_project(target)).status=='BLOCKED'


def test_blocked_state_cannot_pass_even_without_blocker_text(tmp_path):
    compile_project(plan(),tmp_path,True);review(tmp_path)
    p=tmp_path/'.acos/state.yaml';s=read_yaml(p);s['status']='BLOCKED';p.write_bytes(write_yaml_bytes(s))
    assert validate_gate(load_project(tmp_path)).status=='BLOCKED'


def test_completed_requires_handoff_and_all_stages(tmp_path):
    compile_project(plan(),tmp_path,True)
    project=load_project(tmp_path);p=tmp_path/'.acos/state.yaml';s=read_yaml(p)
    s['status']='COMPLETED';s['completed_stages']=['handoff']
    s['gate_reviews']={g['id']:{'decision':'PASS','reviewer':'David','evidence':['context/business_context.md'],'profile_sha256':project.manifest.profile_sha256} for g in project.selection.gates}
    p.write_bytes(write_yaml_bytes(s))
    assert validate_gate(load_project(tmp_path)).status=='BLOCKED'


def test_malformed_gate_cli_returns_blocked(tmp_path,monkeypatch,capsys):
    from acos.cli import main
    compile_project(plan(),tmp_path,True)
    p=tmp_path/'.acos/modules.yaml';s=read_yaml(p);s['gates'][0].pop('stage');p.write_bytes(write_yaml_bytes(s))
    monkeypatch.chdir(tmp_path)
    assert main(['validate'])==4
    assert 'inválido' in capsys.readouterr().out
