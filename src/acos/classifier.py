from pydantic import Field
from .contracts import Model, ProjectProfile
from .catalog import Catalog

class Classification(Model):
    archetypes: list[str] = Field(default_factory=list)
    proposals: list[dict] = Field(default_factory=list)
    unresolved: list[str] = Field(default_factory=list)


def classify(profile: ProjectProfile, catalog: Catalog) -> Classification:
    explicit=profile.engagement.archetypes
    proposals=[{'archetype':a,'rule_id':'declared-archetype','signal':f'engagement.archetypes contiene {a}','certainty':'explicit'} for a in explicit]
    text=' '.join(filter(None,[profile.engagement.decision,profile.engagement.problem])).lower()
    signals={'PRIORITIZE_SELECT':['priorizar','prioritize'], 'OPTIMIZE':['optimizar','optimize'],
             'FORECAST':['forecast','pronosticar'], 'EXPERIMENT_CAUSAL':['uplift','efecto causal'],
             'PREDICT':['predecir','predict'], 'DIAGNOSE':['diagnosticar'], 'SEGMENT':['segmentar'], 'RECOMMEND':['recomendar']}
    for archetype,words in signals.items():
        hit=next((w for w in words if w in text),None)
        if hit and archetype not in explicit:
            proposals.append({'archetype':archetype,'rule_id':'brief-signal','signal':hit,'certainty':'suggested'})
    unresolved=[] if explicit else ['Confirmar arquetipos: el brief no define una clasificación confirmada.']
    return Classification(archetypes=list(explicit),proposals=proposals,unresolved=unresolved)
