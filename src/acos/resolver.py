from dataclasses import dataclass, replace
from pathlib import Path
from .contracts import ProjectProfile, ModuleSelection, ArtifactSpec, Finding, canonical_sha256
from .catalog import Catalog, evaluate_rule
from .foundry import FoundryInventory, SkillRecord

@dataclass
class CompilationPlan:
    profile: ProjectProfile
    selection: ModuleSelection
    artifacts: list[ArtifactSpec]
    skills: list[SkillRecord]
    findings: list[Finding]
    foundry_root: Path | None
    confirmed: bool = False


def resolve(profile: ProjectProfile, catalog: Catalog, inventory: FoundryInventory) -> CompilationPlan:
    modules={m.id:m for m in catalog.modules}
    selected={m.id for m in catalog.modules if evaluate_rule(m.trigger,profile)}
    pending=list(selected)
    while pending:
        name=pending.pop()
        for dep in modules[name].dependencies:
            if dep not in selected: selected.add(dep);pending.append(dep)
    ordered=[m for m in catalog.modules if m.id in selected]
    artifacts={}; gates={}; reasons=[]
    for module in ordered:
        reasons.append({'module':module.id,'signal':module.trigger,'dependencies':module.dependencies})
        for artifact in module.artifacts:
            if artifact.path in artifacts and artifacts[artifact.path]!=artifact:raise ValueError('Conflicto de artifact: '+artifact.path)
            artifacts[artifact.path]=artifact
        for gate in module.gates:
            if gate['id'] in gates and gates[gate['id']]!=gate:raise ValueError('Conflicto de gate')
            gates[gate['id']]=gate
        for playbook in module.playbooks:
            path='playbooks/'+playbook
            artifacts[path]=ArtifactSpec(path=path,template_id='os:'+path,ownership='acos')
    for name in ['project-lifecycle','execution-and-qa','isolation-and-context','capability-lifecycle']:
        path='workflow/'+name+'.md'
        artifacts[path]=ArtifactSpec(path=path,template_id='os:'+path,ownership='acos')
    for name in ['project-and-task','delivery-and-handoff','findings-and-qa']:
        path='templates/'+name+'.md'
        artifacts[path]=ArtifactSpec(path=path,template_id='os:'+path,ownership='human')
    capabilities=[];excluded=[];gaps=[];skills={}
    available={s.name:s for s in inventory.skills}
    for cap in dict.fromkeys(c for m in ordered for c in m.capabilities):
        policy=catalog.capability_policies[cap];conditions=policy['required_characteristics']
        missing=[k for k,v in conditions.items() if profile.data.characteristics.get(k)!=v]
        if conditions.get('ui_required') is True and profile.data.characteristics.get('ui_required') is not True:
            excluded.append({'capability':cap,'reason':'No hay necesidad de interacción UI nueva/modificada confirmada.'})
            continue
        candidates=[available[n] for n in policy['skills'] if n in available]
        compatible=[s for s in candidates if not s.dependencies]
        reason=[]
        if missing:
            excluded.append({'capability':cap,'reason':'Preconditions sin confirmar: '+', '.join(missing)})
            compatible=[];reason.append('Preconditions no confirmadas')
        if candidates and any(s.dependencies for s in candidates):reason.append('Dependencias externas no resueltas')
        if compatible:
            skill=compatible[0];skills[skill.name]=skill
            capabilities.append({'id':cap,'coverage':'skill','skill':skill.name,'status':skill.status,'version':skill.version,'reason':'Propósito y condiciones compatibles con política del catálogo','limits':skill.limits})
        else:
            why='; '.join(reason) or 'Sin skill operativa compatible'
            capabilities.append({'id':cap,'coverage':'partial','artifact':'playbook','reason':why,'limits':policy['limit']})
            gaps.append({'capability':cap,'reason':why,'fallback':policy['fallback'],'limits':policy['limit']})
    selection=ModuleSelection(catalog_version=catalog.version,profile_sha256=canonical_sha256(profile),modules=[m.id for m in ordered],capabilities=capabilities,gates=list(gates.values()),excluded=excluded,gaps=gaps,reasons=reasons)
    return CompilationPlan(profile,selection,list(artifacts.values()),list(skills.values()),inventory.findings,inventory.root)


def preview(plan: CompilationPlan) -> str:
    lines=[f'Proyecto: {plan.profile.project.name}',f'Decisión: {plan.profile.engagement.decision or "Pendiente"}',f'Etapa inicial: {plan.profile.engagement.current_stage}',
           'Módulos: '+', '.join(plan.selection.modules),'Capacidades y cobertura:']
    for cap in plan.selection.capabilities:
        lines.append(f"- {cap['id']}: {cap['coverage']} — {cap['reason']}")
        lines.append('  Límites: '+cap['limits'])
    for skill in plan.skills:
        lines.append(f'- Snapshot {skill.name} {skill.version} [{skill.status}] {skill.source_ref} sha256:{skill.tree_sha256}')
    for finding in plan.findings:lines.append(f'- {finding.code}: {finding.message}')
    for excluded in plan.selection.excluded:lines.append(f"- Excluida {excluded['capability']}: {excluded['reason']}")
    lines.append('Archivos propuestos:')
    from .render import proposed_paths
    lines.extend('  '+p for p in proposed_paths(plan))
    lines.append('Confirmar incluye uso provisional de los snapshots experimentales indicados; no los promueve.')
    return '\n'.join(lines)


def confirm_plan(plan: CompilationPlan, accepted: bool) -> CompilationPlan:
    return replace(plan,confirmed=accepted)
