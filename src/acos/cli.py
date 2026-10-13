"""Entry point local; inicialización requiere confirmación expresa."""
import argparse
import json
from pathlib import Path
from . import __version__
from .contracts import ProjectProfile,AcosError
from .yaml_io import read_yaml
from .config import load_config,save_config
from .catalog import load_catalog
from .classifier import classify
from .foundry import discover_foundry,scan_foundry
from .resolver import resolve,preview,confirm_plan
from .compiler import compile_project,target_directory,inspect_conflicts
from .render import proposed_paths
from .project import load_project,project_status,next_objective
from .gates import validate_gate
from .intake import collect_profile,review_classification
from .llm_adapter import llm_proposal


def accepted(prompt: str) -> bool:
    return input(prompt).strip().lower() in ('s','si','sí','y','yes')


def run_init(args):
    if args.here and args.name:raise AcosError(2,'--here no admite nombre posicional.')
    cfg=load_config();cwd=Path.cwd()
    foundry=discover_foundry(cfg,[cwd/'david-skill-foundry',Path.home()/'david-skill-foundry'])
    if cfg.foundry_path is None:
        if foundry:
            print('Foundry detectado:',foundry)
            if accepted('¿Usar y guardar esta ruta por dispositivo? [s/N]: '):
                cfg.foundry_path=str(foundry);save_config(cfg)
            else:foundry=None
        else:
            value=input('Ruta Foundry local (vacío para continuar sin Foundry): ').strip()
            if value:
                candidate=Path(value).expanduser()
                if not candidate.is_dir():raise AcosError(2,'Foundry no es un directorio accesible.')
                print('Ruta:',candidate)
                if accepted('¿Usar y guardar esta ruta? [s/N]: '):cfg.foundry_path=str(candidate);save_config(cfg);foundry=candidate
    if args.profile_file:
        profile=ProjectProfile.model_validate(read_yaml(Path(args.profile_file)))
        if args.name:
            payload=profile.model_dump();payload['project']['slug']=args.name;profile=ProjectProfile.model_validate(payload)
    else:
        initial=ProjectProfile(project={'slug':args.name,'name':args.name}) if args.name else None
        profile=collect_profile(initial,input)
    print('Perfil propuesto:\n'+json.dumps(profile.model_dump(mode='json'),ensure_ascii=False,indent=2))
    catalog=load_catalog();classification=classify(profile,catalog)
    if args.llm:
        result=llm_proposal(profile,cfg.llm_adapter_argv,lambda msg: (print(msg),accepted('¿Autorizar esta invocación y su payload? [s/N]: '))[1])
        if result:
            classification.proposals+=result.proposals;classification.unresolved+=result.unresolved
        else:print('LLM no disponible/autorizado o salida inválida; continúa clasificación local.')
    print('Clasificación propuesta:\n'+json.dumps(classification.model_dump(),ensure_ascii=False,indent=2))
    profile=review_classification(profile,classification,input)
    plan=resolve(profile,catalog,scan_foundry(foundry))
    target=target_directory(cwd,None if args.here else profile.project.slug,args.here)
    print(preview(plan));print('Destino:',target)
    conflicts=inspect_conflicts(target,{p:b'' for p in proposed_paths(plan) if p!='.acos/manifest.yaml'},args.here)
    if conflicts:raise AcosError(4,'Conflictos antes de escribir: '+', '.join(f.message for f in conflicts))
    if not accepted('¿Confirmar composición y generar workspace? [s/N]: '):raise AcosError(130,'Inicialización cancelada.')
    compile_project(confirm_plan(plan,True),target,args.here)
    print(f'Proyecto listo: {target}\nSiguiente: cd "{target}"\nLee MANUAL.md o ejecuta acos next.')
    for runtime in profile.runtimes:print('Runtime: '+('codex' if runtime=='codex' else 'claude'))
    return 0


class SpanishFormatter(argparse.HelpFormatter):
    def _format_usage(self, usage, actions, groups, prefix):
        return super()._format_usage(usage, actions, groups, prefix or 'Uso: ')


class SpanishParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        kwargs['add_help']=False
        kwargs['formatter_class']=SpanishFormatter
        super().__init__(*args, **kwargs)
        self._positionals.title='Argumentos'
        self._optionals.title='Opciones'
        self.add_argument('-h','--help',action='help',help='Mostrar esta ayuda y salir')


def parser():
    p=SpanishParser(prog='acos',description='Compila y guía proyectos de consultoría Data & AI.')
    p.add_argument('--version',action='version',version=__version__,help='Mostrar versión y salir')
    subs=p.add_subparsers(dest='command',required=True)
    init=subs.add_parser('init',help='Crear workspace tras revisar perfil y composición')
    init.add_argument('name',nargs='?',help='Nombre de subcarpeta nueva')
    init.add_argument('--here',action='store_true',help='Inicializar explícitamente la carpeta actual')
    init.add_argument('--profile-file',help='Perfil YAML canónico como alternativa al wizard')
    init.add_argument('--llm',action='store_true',help='Proponer clasificación con adapter explícito y consentimiento')
    for command,helptext in [('status','Mostrar estado y bloqueos'),('next','Mostrar próximo objetivo'),('validate','Revisar gate sin avanzar estado')]:
        sub=subs.add_parser(command,help=helptext)
        if command=='validate':sub.add_argument('--gate',help='Gate seleccionado a revisar')
    return p


def main(argv: list[str] | None = None) -> int:
    try:
        try:args=parser().parse_args(argv)
        except SystemExit as exc:return int(exc.code)
        if args.command=='init':return run_init(args)
        project=load_project(Path.cwd())
        if args.command in ('status','next'):
            result=project_status(project) if args.command=='status' else next_objective(project)
            print(json.dumps(result,ensure_ascii=False,indent=2))
            return 4 if result['integrity']=='BLOCKED' else 0
        result=validate_gate(project,args.gate)
        print(json.dumps({'status':result.status,'findings':[x.model_dump() for x in result.findings],'evidence':result.evidence},ensure_ascii=False,indent=2))
        return {'PASS':0,'NEEDS_REVIEW':3,'BLOCKED':4}[result.status]
    except (EOFError,KeyboardInterrupt):
        print('Operación cancelada; no se confirmó el workspace.');return 130
    except AcosError as exc:
        print(str(exc));return exc.code
    except (ValueError,OSError) as exc:
        print('Entrada/operación inválida: '+str(exc));return 2
