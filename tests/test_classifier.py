from acos.catalog import load_catalog
from acos.classifier import classify
from acos.contracts import ProjectProfile


def test_rules_use_explicit_signals():
    p=ProjectProfile(project={'slug':'a','name':'A'},engagement={'archetypes':['OPTIMIZE']})
    result=classify(p,load_catalog())
    assert result.archetypes==['OPTIMIZE'] and result.proposals[0]['certainty']=='explicit'


def test_ambiguous_brief_remains_unresolved():
    result=classify(ProjectProfile(project={'slug':'a','name':'A'}),load_catalog())
    assert result.archetypes==[] and result.unresolved


def test_no_ui_or_ml_from_report_delivery():
    result=classify(ProjectProfile(project={'slug':'a','name':'A'},deliverables=['report']),load_catalog())
    assert result.archetypes==[]


def test_missing_label_never_inferred():
    p=ProjectProfile(project={'slug':'a','name':'A'},engagement={'decision':'Priorizar anomalías sin labels'})
    classify(p,load_catalog())
    assert 'labeled' not in p.data.characteristics
