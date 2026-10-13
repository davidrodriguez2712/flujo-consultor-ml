"""Adapter explícito: propuestas tipadas, sin ejecutar acciones sugeridas."""
import json
import subprocess
from pydantic import Field,field_validator
from .contracts import Model,ARCHETYPES
from .classifier import Classification

class Proposal(Model):
    archetypes: list[str]
    reasons: list[str]
    unresolved: list[str] = Field(default_factory=list)

    @field_validator('archetypes')
    @classmethod
    def validate_archetypes(cls,value):
        if any(x not in ARCHETYPES for x in value):raise ValueError('Arquetipo desconocido')
        return list(dict.fromkeys(value))


def llm_proposal(profile, argv: list[str], consent) -> Classification | None:
    if not argv:return None
    payload={'decision':profile.engagement.decision,'problem':profile.engagement.problem,'industry':profile.project.industry,'archetypes':profile.engagement.archetypes}
    encoded=json.dumps(payload,ensure_ascii=False)
    message='Adapter: '+repr(argv)+'\nPuede transmitir este contexto; no incluye archivos de datos ni identidad cliente.\nPayload exacto:\n'+encoded
    if not consent(message):return None
    try:
        proc=subprocess.run(argv,input=encoded,text=True,capture_output=True,shell=False,timeout=30,check=True)
        if len(proc.stdout)>100_000:return None
        proposal=Proposal.model_validate(json.loads(proc.stdout))
        return Classification(archetypes=proposal.archetypes,proposals=[{'archetype':a,'rule_id':'optional-llm','signal':proposal.reasons[i] if i<len(proposal.reasons) else 'Propuesta LLM','certainty':'suggested'} for i,a in enumerate(proposal.archetypes)],unresolved=proposal.unresolved)
    except (OSError,subprocess.SubprocessError,ValueError):return None
