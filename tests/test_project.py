from acos.project import load_project,project_status,next_objective
from acos.compiler import compile_project
from acos.yaml_io import read_yaml,write_yaml_bytes
from test_compiler import plan


def test_state_is_authoritative_over_markdown(tmp_path):
    compile_project(plan(),tmp_path,True)
    p=tmp_path/'.acos/state.yaml';state=read_yaml(p);state['objective']='Nueva tarea';p.write_bytes(write_yaml_bytes(state))
    (tmp_path/'STATE.md').write_text('outdated')
    assert next_objective(load_project(tmp_path))['objective']=='Nueva tarea'


def test_read_commands_preserve_all_bytes(tmp_path):
    compile_project(plan(),tmp_path,True)
    before={p.relative_to(tmp_path):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    project=load_project(tmp_path);project_status(project);next_objective(project)
    assert before=={p.relative_to(tmp_path):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


def test_removed_foundry_does_not_break_project(foundry,tmp_path):
    from conftest import make_skill
    import shutil
    make_skill(foundry);target=tmp_path/'project';compile_project(plan(foundry),target,False)
    shutil.rmtree(foundry)
    assert project_status(load_project(target))['stage']=='discovery'


def completed_project(tmp_path, foundry=None):
    from acos.contracts import STAGES
    from acos.gates import validate_gate
    compile_project(plan(foundry),tmp_path,True)
    project=load_project(tmp_path)
    for gate in project.selection.gates:
        for rel,fields in gate.get('required_fields',{}).items():
            (tmp_path/rel).write_bytes(write_yaml_bytes({key:'Confirmado' for key in fields}))
    path=tmp_path/'.acos/state.yaml';state=read_yaml(path)
    state.update(current_stage='handoff',status='COMPLETED',completed_stages=list(STAGES))
    state['gate_reviews']={g['id']:{'decision':'PASS','reviewer':'David',
        'evidence':['context/business_context.md'],'profile_sha256':project.manifest.profile_sha256}
        for g in project.selection.gates}
    path.write_bytes(write_yaml_bytes(state))
    project=load_project(tmp_path)
    assert validate_gate(project).status=='PASS'
    return project


def test_valid_completion_has_no_pending_work(tmp_path,monkeypatch,capsys):
    import json
    from acos.cli import main
    completed_project(tmp_path)
    before={p.relative_to(tmp_path):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}
    monkeypatch.chdir(tmp_path)
    assert main(['status'])==0
    status=json.loads(capsys.readouterr().out)
    assert status['status']=='COMPLETED' and status['integrity']=='OK'
    assert len(status['completed'])==7
    assert status['next_gates']==[]
    assert main(['next'])==0
    next_=json.loads(capsys.readouterr().out)
    assert next_['status']=='COMPLETED'
    assert next_['questions']==[] and next_['outputs']==[] and next_['gate'] is None
    assert next_['objective']!=read_yaml(tmp_path/'.acos/state.yaml')['objective']
    assert before=={p.relative_to(tmp_path):p.read_bytes() for p in tmp_path.rglob('*') if p.is_file()}


def test_inconsistent_completion_reports_repairs(tmp_path,monkeypatch,capsys):
    import json
    from acos.cli import main
    completed_project(tmp_path)
    # La revisión permanece, pero el contrato obligatorio se ha vaciado.
    (tmp_path/'framing/framing.yaml').write_bytes(write_yaml_bytes({}))
    monkeypatch.chdir(tmp_path)
    for command in ('status','next'):
        assert main([command])==4
        result=json.loads(capsys.readouterr().out)
        assert result['integrity']=='BLOCKED'
        assert any(f['code']=='fields-missing' for f in result['findings'])
        if command=='status':assert result['next_gates']
        else:assert result['gate'] is not None


def test_completion_without_review_is_not_hidden(tmp_path):
    completed_project(tmp_path)
    path=tmp_path/'.acos/state.yaml';state=read_yaml(path)
    state['gate_reviews'].pop('handoff');path.write_bytes(write_yaml_bytes(state))
    result=next_objective(load_project(tmp_path))
    assert result['integrity']=='BLOCKED'
    assert any(f['code']=='completion-unreviewed' for f in result['findings'])
    assert result['gate'] is not None


def test_completed_snapshot_drift_is_not_hidden(foundry,tmp_path):
    from conftest import make_skill
    make_skill(foundry);completed_project(tmp_path,foundry)
    (tmp_path/'.agents/skills/understand-dataset/SKILL.md').write_text('alterado')
    result=next_objective(load_project(tmp_path))
    assert result['integrity']=='BLOCKED'
    assert any(f['code']=='snapshot-integrity' for f in result['findings'])
    assert result['gate'] is not None


def test_active_project_keeps_current_work(tmp_path):
    compile_project(plan(),tmp_path,True)
    project=load_project(tmp_path)
    assert project_status(project)['next_gates']==['discovery']
    next_=next_objective(project)
    assert next_['questions'] and next_['outputs'] and next_['gate']
    assert next_['objective']==project.state.objective
