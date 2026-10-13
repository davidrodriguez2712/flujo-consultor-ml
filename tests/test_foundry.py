import pytest
from acos.foundry import scan_foundry, hash_bundle
from conftest import make_skill


def test_missing_foundry_returns_gap():
    inventory=scan_foundry(None)
    assert not inventory.skills and inventory.findings[0].code=='foundry-missing'


def test_only_operational_roots_scanned(foundry):
    make_skill(foundry)
    make_skill(foundry,'archived',folder='evals')
    assert [s.name for s in scan_foundry(foundry).skills]==['understand-dataset']


def test_scratch_excluded_despite_experimental_metadata(foundry):
    make_skill(foundry,'archive',folder='experiments/scratch')
    assert not scan_foundry(foundry).skills


def test_explicit_knowledge_decision_excludes_match(foundry):
    make_skill(foundry)
    (foundry/'candidates').mkdir()
    (foundry/'candidates'/'decision.md').write_text('---\nname: understand-dataset\nid: acos-understand-dataset\n---\n# Decisión\n\nEstado: **mantener como conocimiento**\n')
    inventory=scan_foundry(foundry)
    assert not inventory.skills and any(f.code=='decision-excluded' for f in inventory.findings)


def test_bad_frontmatter_excluded(foundry):
    p=make_skill(foundry);(p/'SKILL.md').write_text('not metadata')
    assert not scan_foundry(foundry).skills


def test_resource_symlink_escape_rejected(foundry,tmp_path):
    p=make_skill(foundry);(p/'escape').symlink_to(tmp_path)
    with pytest.raises(ValueError): hash_bundle(p)
    assert not scan_foundry(foundry).skills


def test_bundle_hash_stable_and_detects_resource_change(foundry):
    p=make_skill(foundry);(p/'notes.md').write_text('one')
    initial,files=hash_bundle(p)
    assert initial==hash_bundle(p)[0] and len(files)==2
    (p/'notes.md').write_text('two')
    assert hash_bundle(p)[0]!=initial


def test_conflicting_operational_records_are_not_auto_selected(foundry):
    make_skill(foundry);make_skill(foundry,status='stable',folder='stable')
    inventory=scan_foundry(foundry)
    assert not inventory.skills and any(f.code=='duplicate-skill' for f in inventory.findings)


def test_hidden_resource_is_included_and_hashed(foundry):
    root=make_skill(foundry)
    (root/'.config.yaml').write_text('threshold: 1\n')
    with (root/'SKILL.md').open('a') as out:out.write('\n[Configuración](.config.yaml)\n')
    skill=scan_foundry(foundry).skills[0]
    assert '.config.yaml' in [f['relative_path'] for f in skill.files]
    old=skill.tree_sha256;(root/'.config.yaml').write_text('threshold: 2\n')
    assert hash_bundle(root)[0]!=old


@pytest.mark.parametrize('decision',['rechazado','no usar','decisión desconocida'])
def test_non_operational_or_unknown_decision_excludes_skill(foundry,decision):
    make_skill(foundry);(foundry/'candidates').mkdir()
    (foundry/'candidates'/'decision.md').write_text(f'---\nname: understand-dataset\nid: acos-understand-dataset\n---\n# Decisión\nEstado: **{decision}**\n')
    assert not scan_foundry(foundry).skills


def test_status_and_version_accepted_under_metadata_block(foundry):
    p=make_skill(foundry)
    (p/'SKILL.md').write_text('---\nname: understand-dataset\ndescription: Procedimiento de prueba\nmetadata:\n  status: experimental\n  version: 0.2.2\n  domain: data-science\n---\n# Límites\nSolo prueba.\n')
    skills=scan_foundry(foundry).skills
    assert [(s.name,s.status,s.version) for s in skills]==[('understand-dataset','experimental','0.2.2')]


def test_root_metadata_takes_precedence_and_bad_metadata_block_excluded(foundry):
    p=make_skill(foundry)
    (p/'SKILL.md').write_text('---\nname: understand-dataset\nstatus: experimental\nversion: 0.1.0\nmetadata:\n  status: stable\n  version: 9.9.9\n---\nx\n')
    assert [s.version for s in scan_foundry(foundry).skills]==['0.1.0']
    (p/'SKILL.md').write_text('---\nname: understand-dataset\nmetadata: texto\n---\nx\n')
    assert not scan_foundry(foundry).skills
