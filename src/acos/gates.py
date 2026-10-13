"""Checks declarativos y revisión trazable; ninguna ejecución de código del proyecto."""
from dataclasses import dataclass
from pathlib import Path
from .contracts import Finding,STAGES,canonical_sha256
from .compiler import safe_relative,reject_symlinks
from .foundry import hash_bundle
from .yaml_io import read_yaml

@dataclass
class GateResult:
    status: str
    findings: list[Finding]
    evidence: list[str]


def checked_path(project,rel: str) -> Path:
    path=project.root/safe_relative(rel);reject_symlinks(path)
    if not path.resolve().is_relative_to(project.root.resolve()):raise ValueError('Escape del workspace')
    return path


def review_valid(project,gate) -> bool:
    review=project.state.gate_reviews.get(gate['id'])
    if not review or review.decision!='PASS' or not review.reviewer.strip() or not review.evidence or review.profile_sha256!=project.manifest.profile_sha256:return False
    try:return all(checked_path(project,p).is_file() and checked_path(project,p).stat().st_size>0 for p in review.evidence)
    except (ValueError,OSError):return False


def integrity_findings(project) -> list[Finding]:
    result=[]
    def add(code,message):result.append(Finding(code=code,message=message))
    if canonical_sha256(project.profile)!=project.manifest.profile_sha256 or project.selection.profile_sha256!=project.manifest.profile_sha256:add('profile-drift','Perfil cambió; revisar/recompilar en workspace nuevo.')
    if canonical_sha256(project.selection)!=project.manifest.modules_sha256:add('modules-drift','Composición cambió después de inicializar.')
    if project.state.blockers or project.state.status=='BLOCKED':add('state-blocked','Resolver estado/bloqueos registrados antes de avanzar.')
    initial=STAGES.index(project.profile.engagement.current_stage);current=STAGES.index(project.state.current_stage)
    if current<initial:add('stage-regression','Retroceso de etapa requiere revisión explícita del contexto de entrada.')
    for stage in STAGES[initial:current]:
        prior=[g for g in project.selection.gates if g['stage']==stage]
        if stage not in project.state.completed_stages or not all(review_valid(project,g) for g in prior):add('stage-sequence',f'Etapa previa sin aprobación: {stage}')
    if any(STAGES.index(stage)>current for stage in project.state.completed_stages):
        add('stage-sequence','Etapas futuras declaradas completas antes de alcanzarlas.')
    if project.state.completed_stages != sorted(project.state.completed_stages,key=STAGES.index):
        add('stage-sequence','Etapas completadas fuera de secuencia.')
    required=STAGES[initial:]
    if project.state.status=='COMPLETED' and (project.state.current_stage!='handoff' or not set(required).issubset(project.state.completed_stages) or not all(review_valid(project,g) for g in project.selection.gates)):

        add('completion-unreviewed','Cierre declarado sin gates aprobados.')
    for skill in project.manifest.skills:
        try:
            for relative in skill['runtime_paths']:
                path=checked_path(project,relative)
                if hash_bundle(path)[0]!=skill['tree_sha256']:add('snapshot-integrity',skill['name']+': snapshot alterado o ausente.')
        except (ValueError,OSError,KeyError):add('snapshot-integrity','Snapshot inválido/ausente.')
    return result


def structural_findings(project,gate) -> list[Finding]:
    result=[]
    for rel in gate.get('artifacts',[]):
        try:
            path=checked_path(project,rel)
            if not path.is_file() or path.stat().st_size==0:
                result.append(Finding(code='artifact-missing',message='Falta output: '+rel,paths=[rel]));continue
            required=gate.get('required_fields',{}).get(rel,[])
            if required:
                values=read_yaml(path)
                missing=[key for key in required if values.get(key) is None or values.get(key)=='' or values.get(key)==[] or values.get(key)=={}]
                if missing:result.append(Finding(code='fields-missing',message=f'{rel}: completar '+', '.join(missing),paths=[rel]))
        except (ValueError,OSError) as exc:result.append(Finding(code='artifact-invalid',message=str(exc),paths=[rel]))
    return result


def validate_gate(project,gate_id: str | None = None) -> GateResult:
    findings=integrity_findings(project);evidence=[]
    if findings:return GateResult('BLOCKED',findings,evidence)
    gates=[g for g in project.selection.gates if g['id']==gate_id] if gate_id else [g for g in project.selection.gates if g['stage']==project.state.current_stage]
    if not gates:return GateResult('BLOCKED',findings+[Finding(code='unknown-gate',message='Gate no seleccionado/desconocido.')],[])
    targetindex=max(STAGES.index(g['stage']) for g in gates)
    # Entry at a later stage does not pretend previous artifacts/evidence are complete.
    for gate in project.selection.gates:
        if STAGES.index(gate['stage'])<=targetindex:
            findings.extend(structural_findings(project,gate))
    if findings:return GateResult('BLOCKED',findings,evidence)
    needs_review=[]
    for gate in gates:
        if gate.get('human_review',True) and not review_valid(project,gate):
            needs_review.append(Finding(code='human-review',message='Revisión/evidencia pendiente para '+gate['id']))
        else:
            review=project.state.gate_reviews.get(gate['id'])
            if review:evidence.extend(review.evidence)
    return GateResult('NEEDS_REVIEW' if needs_review else 'PASS',needs_review,list(dict.fromkeys(evidence)))
