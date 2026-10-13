import pytest
from acos.catalog import load_catalog, evaluate_rule
from acos.contracts import ProjectProfile


def test_catalog_reference_integrity():
    c=load_catalog()
    assert c.version=='0.1.0' and len(c.modules)==15
    for m in c.modules:
        assert all(a.template_id in c.templates for a in m.artifacts)
        assert all(dep in {x.id for x in c.modules} for dep in m.dependencies)


def test_overlapping_modules_deduplicate_artifacts():
    c=load_catalog()
    assert len({m.id for m in c.modules})==len(c.modules)
    core=next(m for m in c.modules if m.id=='consulting_core')
    assert 'framing/framing.yaml' in [a.path for a in core.artifacts]


def test_invalid_catalog_operator_rejected():
    with pytest.raises(ValueError): evaluate_rule({'operator':'exec','field':'project.name'},ProjectProfile(project={'slug':'a','name':'A'}))
