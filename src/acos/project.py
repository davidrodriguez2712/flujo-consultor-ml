from dataclasses import dataclass
from pathlib import Path
from .contracts import ProjectProfile,ModuleSelection,ProjectState,Manifest,AcosError,STAGES
from .yaml_io import read_yaml
from .compiler import reject_symlinks
from .render import QUESTIONS

@dataclass
class ProjectView:
    profile: ProjectProfile
    selection: ModuleSelection
    state: ProjectState
    manifest: Manifest
    root: Path


def load_project(root: Path) -> ProjectView:
    try:
        models=[]
        for name,model in [('project-profile',ProjectProfile),('modules',ModuleSelection),('state',ProjectState),('manifest',Manifest)]:
            path=root/'.acos'/f'{name}.yaml';reject_symlinks(path)
            models.append(model.model_validate(read_yaml(path)))
        return ProjectView(*models,root)
    except (ValueError,OSError) as exc:raise AcosError(4,f'Workspace incompleto/inválido: {exc}') from exc


def project_findings(project: ProjectView) -> list:
    from .gates import integrity_findings,validate_gate
    if project.state.status=='COMPLETED':
        # El cierre exige también los contratos estructurales de todas las etapas.
        return validate_gate(project).findings
    return integrity_findings(project)


def project_status(project: ProjectView) -> dict:
    from .gates import validate_gate
    findings=project_findings(project)
    closed=project.state.status=='COMPLETED' and not findings
    completed=[]
    for stage in project.state.completed_stages:
        gates=[g for g in project.selection.gates if g['stage']==stage]
        if gates and all(validate_gate(project,g['id']).status=='PASS' for g in gates):completed.append(stage)
    return {'project':project.profile.project.name,'stage':project.state.current_stage,'status':project.state.status,
            'completed':completed,'total_stages':len(STAGES)-STAGES.index(project.profile.engagement.current_stage),
            'blockers':project.state.blockers,'open_decisions':project.state.open_decisions,
            'next_gates':[] if closed else [g['id'] for g in project.selection.gates if g['stage']==project.state.current_stage],
            'integrity':'BLOCKED' if findings else 'OK','findings':[f.model_dump() for f in findings]}


def next_objective(project: ProjectView) -> dict:
    stage=project.state.current_stage
    findings=project_findings(project)
    completed=project.state.status=='COMPLETED'
    closed=completed and not findings
    objective=project.state.objective
    if closed:objective='Proyecto completado; no hay una siguiente etapa.'
    elif completed:objective='Resolver los hallazgos del cierre antes de considerar completado el proyecto.'
    return {'stage':stage,'status':project.state.status,'objective':objective,
            'questions':[] if closed else QUESTIONS[stage],
            'outputs':[] if closed else list(dict.fromkeys(path for g in project.selection.gates if g['stage']==stage for path in g['artifacts'])),
            'capabilities':project.selection.capabilities,'gaps':project.selection.gaps,
            'gate':None if closed else ('Corregir los hallazgos y volver a validar el cierre.' if completed else 'Obtener evidencia y revisión humana antes de registrar un avance de etapa.'),
            'integrity':'BLOCKED' if findings else 'OK','findings':[f.model_dump() for f in findings]}
