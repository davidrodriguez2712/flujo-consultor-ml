"""Catálogo declarativo; no ejecuta expresiones ni código de YAML."""
from importlib.resources import files
from pydantic import Field
from .contracts import Model, ArtifactSpec, ProjectProfile
from .yaml_io import parse_yaml

class ModuleSpec(Model):
    id: str
    version: str
    trigger: dict
    dependencies: list[str] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    artifacts: list[ArtifactSpec] = Field(default_factory=list)
    gates: list[dict] = Field(default_factory=list)
    playbooks: list[str] = Field(default_factory=list)

class Catalog(Model):
    version: str
    modules: list[ModuleSpec]
    templates: dict[str,str]
    capability_policies: dict[str,dict]


def profile_value(profile: ProjectProfile, field: str):
    value=profile.model_dump()
    for part in field.split('.'):
        if not isinstance(value,dict): raise ValueError('Campo de regla inválido')
        value=value.get(part)
    return value


def evaluate_rule(rule: dict, profile: ProjectProfile) -> bool:
    op=rule.get('operator')
    if op in ('all','any'):
        values=[evaluate_rule(child,profile) for child in rule['rules']]
        return all(values) if op=='all' else any(values)
    if op not in ('equals','contains','is_true'): raise ValueError(f'Operador no permitido: {op}')
    value=profile_value(profile,rule['field'])
    if op=='is_true': return value is True
    if op=='equals': return value==rule.get('value')
    if not isinstance(value,(list,str)): return False
    return rule.get('value') in value


def load_catalog() -> Catalog:
    catalog=Catalog.model_validate(parse_yaml(files('acos').joinpath('resources/catalog.yaml').read_text(encoding='utf-8')))
    ids=[m.id for m in catalog.modules]
    if len(ids)!=len(set(ids)): raise ValueError('IDs duplicados en catálogo')
    probe=ProjectProfile(project={'slug':'probe','name':'Probe'})
    for module in catalog.modules:
        evaluate_rule(module.trigger,probe)
        if any(dep not in ids for dep in module.dependencies): raise ValueError('Dependencia de módulo ausente')
        if any(a.template_id not in catalog.templates for a in module.artifacts): raise ValueError('Template ausente')
        if any(c not in catalog.capability_policies for c in module.capabilities): raise ValueError('Política de capacidad ausente')
    return catalog
