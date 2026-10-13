"""Contratos persistentes y errores de dominio; no contienen paths del dispositivo."""
import hashlib
import json
import re
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field, field_validator

ARCHETYPES = ['DIAGNOSE','PREDICT','FORECAST','PRIORITIZE_SELECT','OPTIMIZE','EXPERIMENT_CAUSAL','SEGMENT','RECOMMEND']
STAGES = ['discovery','framing','diagnosis','execution','validation','delivery','handoff']
RUNTIMES = ['codex','claude_code']


def valid_slug(value: str) -> str:
    reserved = {'con','prn','aux','nul', *[f'com{i}' for i in range(1,10)], *[f'lpt{i}' for i in range(1,10)]}
    if not re.fullmatch(r'[a-z0-9][a-z0-9-]{0,63}',value) or value.lower().split('.')[0] in reserved:
        raise ValueError('Slug inválido: usar minúsculas, números y guiones; evitar nombres reservados Windows.')
    return value


class Model(BaseModel):
    model_config = ConfigDict(extra='forbid', strict=True, validate_assignment=True)


class Versioned(Model):
    schema_version: Literal[1] = 1

    @field_validator('schema_version', mode='before')
    @classmethod
    def schema(cls, value):
        if type(value) is not int or value != 1: raise ValueError('schema_version no soportado')
        return value


class ProjectIdentity(Model):
    slug: str
    name: str = Field(min_length=1)
    client: str | None = None
    industry: str | None = None
    market: str | None = None
    role: str | None = None
    _slug = field_validator('slug')(valid_slug)


class Engagement(Model):
    decision: str | None = None
    problem: str | None = None
    success_metric: str | None = None
    decision_owner: str | None = None
    users: str | None = None
    archetypes: list[str] = Field(default_factory=list)
    delivery_modes: list[str] = Field(default_factory=lambda: ['analysis'])
    current_stage: str = 'discovery'
    open_questions: list[str] = Field(default_factory=list)

    @field_validator('archetypes')
    @classmethod
    def archetypes_valid(cls, value):
        if any(x not in ARCHETYPES for x in value): raise ValueError('Arquetipo desconocido')
        return list(dict.fromkeys(value))

    @field_validator('current_stage')
    @classmethod
    def stage_valid(cls, value):
        if value not in STAGES: raise ValueError('Etapa desconocida')
        return value

    @field_validator('delivery_modes')
    @classmethod
    def modes_valid(cls, value):
        if any(x not in ['analysis','research','automation','product','production','software'] for x in value):
            raise ValueError('Forma de entrega desconocida')
        return value


class DataContext(Model):
    sources: list[str] = Field(default_factory=list)
    characteristics: dict[str, bool | str | list[str]] = Field(default_factory=dict)


class ProjectProfile(Versioned):
    project: ProjectIdentity
    engagement: Engagement = Field(default_factory=Engagement)
    data: DataContext = Field(default_factory=DataContext)
    constraints: list[str] = Field(default_factory=list)
    deliverables: list[str] = Field(default_factory=list)
    runtimes: list[str] = Field(default_factory=lambda: ['codex','claude_code'])

    @field_validator('runtimes')
    @classmethod
    def runtimes_valid(cls,value):
        if not value or any(x not in RUNTIMES for x in value): raise ValueError('Runtime desconocido o vacío')
        return list(dict.fromkeys(value))


class GateSpec(Model):
    id: str = Field(min_length=1)
    stage: str
    artifacts: list[str]
    required_fields: dict[str,list[str]]
    human_review: bool

    @field_validator('stage')
    @classmethod
    def stage_valid(cls,value):
        if value not in STAGES:raise ValueError('Etapa de gate desconocida')
        return value


class ModuleSelection(Versioned):
    catalog_version: str
    profile_sha256: str
    modules: list[str] = Field(default_factory=list)
    capabilities: list[dict] = Field(default_factory=list)
    gates: list[dict] = Field(default_factory=list)
    excluded: list[dict] = Field(default_factory=list)
    gaps: list[dict] = Field(default_factory=list)
    reasons: list[dict] = Field(default_factory=list)

    @field_validator('gates')
    @classmethod
    def gates_valid(cls,value):
        parsed=[GateSpec.model_validate(g).model_dump() for g in value]
        ids=[g['id'] for g in parsed]
        if len(ids)!=len(set(ids)):raise ValueError('IDs de gate duplicados')
        return parsed


class GateReview(Model):
    decision: Literal['PASS','NEEDS_REVIEW','BLOCKED']
    reviewer: str
    evidence: list[str]
    profile_sha256: str


class ProjectState(Versioned):
    current_stage: str
    status: Literal['NOT_STARTED','IN_PROGRESS','BLOCKED','COMPLETED'] = 'NOT_STARTED'
    objective: str
    completed_stages: list[str] = Field(default_factory=list)
    blockers: list[str] = Field(default_factory=list)
    open_decisions: list[str] = Field(default_factory=list)
    gate_reviews: dict[str,GateReview] = Field(default_factory=dict)

    @field_validator('current_stage')
    @classmethod
    def stage_valid(cls,v):
        if v not in STAGES: raise ValueError('Etapa desconocida')
        return v

    @field_validator('completed_stages')
    @classmethod
    def stages_valid(cls,v):
        if len(v)!=len(set(v)) or any(x not in STAGES for x in v): raise ValueError('Etapas completadas inválidas')
        return v


class Manifest(Versioned):
    acos_version: str
    catalog_version: str
    profile_sha256: str
    modules_sha256: str
    source_os_version: str = '2.0'
    artifacts: list[dict] = Field(default_factory=list)
    skills: list[dict] = Field(default_factory=list)
    initialization: Literal['complete'] = 'complete'


class UserConfig(Versioned):
    foundry_path: str | None = None
    llm_adapter_argv: list[str] = Field(default_factory=list)


class ArtifactSpec(Model):
    path: str
    template_id: str
    ownership: str = 'human'


class Finding(Model):
    code: str
    message: str
    paths: list[str] = Field(default_factory=list)


class AcosError(ValueError):
    def __init__(self, code: int, message: str):
        super().__init__(message)
        self.code = code


def canonical_sha256(model: BaseModel) -> str:
    data=json.dumps(model.model_dump(mode='json'),sort_keys=True,ensure_ascii=False,separators=(',',':'))
    return hashlib.sha256(data.encode()).hexdigest()
