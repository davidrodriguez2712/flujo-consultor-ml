from acos.catalog import load_catalog
from acos.contracts import ProjectProfile
from acos.foundry import scan_foundry
from acos.resolver import resolve, preview, confirm_plan
from conftest import make_skill


def profile(**kwargs):
    return ProjectProfile(project={'slug':'fraude','name':'Fraude'},**kwargs)


def test_fraud_composes_data_selection_optimization_without_genai():
    plan=resolve(profile(engagement={'archetypes':['PREDICT','PRIORITIZE_SELECT','OPTIMIZE']},data={'sources':['csv'],'characteristics':{'labeled':'partial','supervised':True}}),load_catalog(),scan_foundry(None))
    assert set(plan.selection.modules)=={'consulting_core','data_analysis','supervised_model','selection','optimization'}
    assert not plan.confirmed


def test_research_omits_modeling():
    plan=resolve(profile(engagement={'delivery_modes':['research']}),load_catalog(),scan_foundry(None))
    assert plan.selection.modules==['consulting_core','research']


def test_unlabeled_anomaly_not_supervised_by_default():
    plan=resolve(profile(engagement={'archetypes':['DIAGNOSE','PRIORITIZE_SELECT']},data={'sources':['csv'],'characteristics':{'labeled':'no'}}),load_catalog(),scan_foundry(None))
    assert 'supervised_model' not in plan.selection.modules


def test_ui_preconditions_not_assumed(foundry):
    make_skill(foundry,'figma-handoff')
    plan=resolve(profile(engagement={'delivery_modes':['product']}),load_catalog(),scan_foundry(foundry))
    assert not plan.skills and any(x['capability']=='figma-handoff' for x in plan.selection.excluded)


def test_experimental_requires_visible_confirmation(foundry):
    make_skill(foundry)
    plan=resolve(profile(data={'sources':['csv']}),load_catalog(),scan_foundry(foundry))
    assert len(plan.skills)==1 and 'experimental' in preview(plan)
    assert not plan.confirmed and confirm_plan(plan,True).confirmed


def test_deferred_or_knowledge_not_operational(foundry):
    make_skill(foundry,'reconcile-business-metrics')
    plan=resolve(profile(),load_catalog(),scan_foundry(foundry))
    assert not plan.skills


def test_missing_foundry_preserves_os_fallback():
    plan=resolve(profile(),load_catalog(),scan_foundry(None))
    assert plan.artifacts and plan.selection.gaps


def test_init_at_validation_keeps_prior_requirements_visible():
    plan=resolve(profile(engagement={'current_stage':'validation'}),load_catalog(),scan_foundry(None))
    assert any(g['id']=='framing' for g in plan.selection.gates)
    assert 'framing/framing.yaml' in [a.path for a in plan.artifacts]


def test_api_without_ui_does_not_require_ui_capabilities():
    p=profile(engagement={'delivery_modes':['software']},deliverables=['api'])
    plan=resolve(p,load_catalog(),scan_foundry(None))
    ids={c['id'] for c in plan.selection.capabilities}
    assert 'software-design' in ids
    assert not {'ui-planning','figma-handoff','visual-qa'} & ids
    assert not any(g['capability'] in {'ui-planning','figma-handoff','visual-qa'} for g in plan.selection.gaps)
