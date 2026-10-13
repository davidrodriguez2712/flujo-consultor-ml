from acos.contracts import ProjectProfile,ProjectState
from acos.catalog import load_catalog
from acos.foundry import scan_foundry
from acos.resolver import resolve
from acos.render import render_project


def test_manual_is_business_specific():
    p=ProjectProfile(project={'slug':'fraude','name':'Fraude eléctrico'},engagement={'decision':'Priorizar inspecciones mensuales','current_stage':'framing'})
    plan=resolve(p,load_catalog(),scan_foundry(None))
    rendered=render_project(plan,ProjectState(current_stage='framing',objective='Definir KPI'))
    assert 'Priorizar inspecciones mensuales' in rendered['MANUAL.md'].decode()
    assert b'.acos/state.yaml' in rendered['AGENTS.md']
    assert rendered['CLAUDE.md'].decode().count('AGENTS.md')==1


def test_no_absolute_foundry_paths(foundry):
    from conftest import make_skill
    make_skill(foundry)
    p=ProjectProfile(project={'slug':'a','name':'A'},data={'sources':['csv']})
    plan=resolve(p,load_catalog(),scan_foundry(foundry))
    data=render_project(plan,ProjectState(current_stage='discovery',objective='Inicio'))
    assert all(str(foundry).encode() not in value for value in data.values())
