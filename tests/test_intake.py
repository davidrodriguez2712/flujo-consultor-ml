from acos.intake import collect_profile,review_classification
from acos.classifier import classify
from acos.catalog import load_catalog
from acos.contracts import ProjectProfile
import pytest


def test_wizard_core_questions_at_most_twelve():
    prompts=[]
    def ask(q):prompts.append(q);return 'research-case' if 'Nombre' in q else ''
    result=collect_profile(None,ask)
    assert result.project.slug=='research-case' and len(prompts)==12


def test_conditional_questions_only_when_relevant():
    prompts=[]
    def ask(q):prompts.append(q);return 'a' if 'Nombre' in q else ''
    collect_profile(None,ask)
    assert not any('Label' in q or 'Figma' in q for q in prompts)


def test_eof_and_ctrl_c_never_confirm():
    p=ProjectProfile(project={'slug':'a','name':'A'})
    def ask(q):raise EOFError
    with pytest.raises(EOFError): review_classification(p,classify(p,load_catalog()),ask)
