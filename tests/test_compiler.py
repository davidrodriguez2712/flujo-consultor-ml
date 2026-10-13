import pytest
from pathlib import Path
from acos.contracts import ProjectProfile,AcosError
from acos.catalog import load_catalog
from acos.foundry import scan_foundry
from acos.resolver import resolve,confirm_plan
from acos.compiler import compile_project
from conftest import make_skill


def plan(foundry=None):
    return confirm_plan(resolve(ProjectProfile(project={'slug':'a','name':'A'},data={'sources':['csv']}),load_catalog(),scan_foundry(foundry)),True)


def test_manifest_written_last(tmp_path,monkeypatch):
    import acos.compiler as compiler
    writes=[];original=compiler.write_exclusive
    def track(path,data):writes.append(path.name);return original(path,data)
    monkeypatch.setattr(compiler,'write_exclusive',track)
    compile_project(plan(),tmp_path/'project',False)
    assert writes[-1]=='manifest.yaml'


def test_cancelled_plan_writes_nothing(tmp_path):
    p=plan();p.confirmed=False
    with pytest.raises(AcosError):compile_project(p,tmp_path/'project',False)
    assert not (tmp_path/'project').exists()


def test_existing_target_blocked(tmp_path):
    with pytest.raises(AcosError):compile_project(plan(),tmp_path,False)


def test_here_preserves_unrelated_files(tmp_path):
    (tmp_path/'mine.txt').write_text('mine')
    compile_project(plan(),tmp_path,True)
    assert (tmp_path/'mine.txt').read_text()=='mine'


def test_here_collision_writes_nothing(tmp_path):
    (tmp_path/'MANUAL.md').write_text('existing')
    with pytest.raises(AcosError):compile_project(plan(),tmp_path,True)
    assert sorted(p.name for p in tmp_path.iterdir())==['MANUAL.md']


def test_failure_rolls_back_only_own_files(tmp_path,monkeypatch):
    import acos.compiler as compiler
    (tmp_path/'mine').write_text('keep')
    real=compiler.write_exclusive
    def fail(path,data):
        if path.name=='MANUAL.md':raise OSError('simulated')
        return real(path,data)
    monkeypatch.setattr(compiler,'write_exclusive',fail)
    with pytest.raises(AcosError):compile_project(plan(),tmp_path,True)
    assert sorted(p.name for p in tmp_path.iterdir())==['mine']


def test_foundry_mutation_after_preview_blocks_commit(foundry,tmp_path):
    skill=make_skill(foundry);p=plan(foundry)
    (skill/'SKILL.md').write_text('changed')
    with pytest.raises(AcosError):compile_project(p,tmp_path/'project',False)
    assert not (tmp_path/'project').exists()


def test_decision_change_after_preview_requires_reconfirmation(foundry,tmp_path):
    make_skill(foundry);p=plan(foundry);(foundry/'candidates').mkdir()
    (foundry/'candidates'/'decision.md').write_text('---\nname: understand-dataset\nid: acos-understand-dataset\n---\n# Decisión\nEstado: **mantener como conocimiento**\n')
    with pytest.raises(AcosError):compile_project(p,tmp_path/'project',False)


def test_bundle_resources_identical_for_both_runtimes(foundry,tmp_path):
    s=make_skill(foundry);(s/'reference.md').write_text('resource')
    target=tmp_path/'project';manifest=compile_project(plan(foundry),target,False)
    a=target/'.agents/skills/understand-dataset/reference.md';b=target/'.claude/skills/understand-dataset/reference.md'
    assert a.read_bytes()==b.read_bytes()==b'resource'
    assert len(manifest.skills[0]['runtime_paths'])==2


def test_new_project_includes_delivery_handoff_template(tmp_path):
    target=tmp_path/'project'
    manifest=compile_project(plan(),target,False)
    template=target/'templates/delivery-and-handoff.md'
    assert template.is_file()
    assert any(entry['path']=='templates/delivery-and-handoff.md' for entry in manifest.artifacts)


def test_new_project_includes_findings_qa_template(tmp_path):
    target=tmp_path/'project'
    manifest=compile_project(plan(),target,False)
    assert (target/'templates/findings-and-qa.md').is_file()
    assert any(entry['path']=='templates/findings-and-qa.md' for entry in manifest.artifacts)


def test_new_project_installs_task_contract_template_with_integrity_tracking(tmp_path):
    # Rompe si el compiler omite el contrato necesario o instala una copia obsoleta.
    import hashlib
    target=tmp_path/'project'
    manifest=compile_project(plan(),target,False)
    template=target/'templates/project-and-task.md'
    assert template.is_file()
    canonical=Path(__file__).parents[1]/'templates/project-and-task.md'
    assert template.read_bytes()==canonical.read_bytes()
    entry=next(e for e in manifest.artifacts if e['path']=='templates/project-and-task.md')
    assert entry['initial_sha256']==hashlib.sha256(template.read_bytes()).hexdigest()
