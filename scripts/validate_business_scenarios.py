"""Simulaciones sintéticas del compiler; no evalúan eficacia de skills o negocio."""
import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path

from acos.catalog import load_catalog
from acos.compiler import compile_project
from acos.contracts import ProjectProfile, STAGES
from acos.foundry import scan_foundry
from acos.gates import validate_gate
from acos.project import load_project, next_objective, project_status
from acos.resolver import confirm_plan, resolve
from acos.yaml_io import read_yaml, write_yaml_bytes


CASES = [
    ('fraude-electrico', ['PREDICT','PRIORITIZE_SELECT','OPTIMIZE'], ['supervised_model','selection','optimization'], {}),
    ('riesgo-credito', ['PREDICT','PRIORITIZE_SELECT'], ['supervised_model','selection'], {}),
    ('churn', ['PREDICT','PRIORITIZE_SELECT'], ['supervised_model','selection'], {}),
    ('clv', ['PREDICT','OPTIMIZE'], ['supervised_model','optimization'], {}),
    ('uplift', ['EXPERIMENT_CAUSAL','PRIORITIZE_SELECT'], ['intervention','selection'], {'supervised':False,'labeled':'partial'}),
    ('anomalias-sin-labels', ['DIAGNOSE','PRIORITIZE_SELECT'], ['selection'], {'supervised':False,'labeled':'no'}),
    ('forecast-demanda', ['FORECAST'], ['forecast'], {'supervised':False}),
    ('inventario', ['FORECAST','OPTIMIZE'], ['forecast','optimization'], {'supervised':False}),
    ('pricing', ['EXPERIMENT_CAUSAL','OPTIMIZE'], ['intervention','optimization'], {'supervised':False}),
    ('segmentacion', ['SEGMENT'], ['segmentation'], {'supervised':False}),
    ('recomendaciones', ['RECOMMEND'], ['recommendation'], {'supervised':False}),
    ('rutas', ['OPTIMIZE'], ['optimization'], {'supervised':False,'geospatial':True}),
    ('staffing', ['FORECAST','OPTIMIZE'], ['forecast','optimization'], {'supervised':False}),
    ('experimento-ab', ['EXPERIMENT_CAUSAL'], ['intervention'], {'supervised':False}),
    ('causal-observacional', ['EXPERIMENT_CAUSAL'], ['intervention'], {'supervised':False,'assignment':'observational'}),
    ('entrada-mercado', ['DIAGNOSE'], ['research'], {'research':True}),
    ('rag', ['RECOMMEND'], ['genai_solution','recommendation'], {'genai':True,'supervised':False}),
    ('extraccion-documentos', ['DIAGNOSE'], ['genai_solution'], {'genai':True,'supervised':False}),
    ('api-sin-ui', ['PREDICT'], ['software_ui','supervised_model'], {'software':True,'ui_required':False}),
    ('dashboard', ['DIAGNOSE'], ['software_ui'], {'software':True,'ui_required':True,'supervised':False}),
    ('figma-handoff', ['RECOMMEND'], ['software_ui','recommendation'], {'software':True,'ui_required':True,'figma':True,'design_system':True,'stack':'react-shadcn'}),
    ('visual-qa', ['DIAGNOSE'], ['software_ui'], {'software':True,'ui_required':True,'implemented_ui':True,'orca':True}),
    ('modelo-heredado', ['PREDICT'], ['supervised_model'], {'entry':'validation'}),
    ('modelo-produccion', ['PREDICT'], ['supervised_model','operationalization'], {'production':True,'feature_design':True}),
]


def digest_tree(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def run(foundry=None):
    catalog = load_catalog()
    inventory = scan_foundry(foundry)
    results = []
    with tempfile.TemporaryDirectory(prefix='acos-simulations-') as directory:
        root = Path(directory).resolve()
        for slug, archetypes, required, options in CASES:
            characteristics = {'supervised':True,'labeled':'yes','temporal':True,'panel':True}
            characteristics.update({k:v for k,v in options.items() if k not in ('entry','software','research','production')})
            profile = ProjectProfile(project={'slug':slug,'name':slug},
                engagement={'decision':'Decisión sintética: '+slug, 'success_metric':'valor esperado',
                    'decision_owner':'Revisor sintético', 'archetypes':archetypes,
                    'current_stage':options.get('entry','discovery'),
                    'delivery_modes':['research' if options.get('research') else 'software' if options.get('software') else 'production' if options.get('production') else 'analysis']},
                data={'sources':[] if options.get('research') else ['csv'], 'characteristics':characteristics},
                deliverables=['decision_memo','business_case'])
            plan = resolve(profile,catalog,inventory)
            assert set(required) <= set(plan.selection.modules), slug
            if not characteristics['supervised']:
                assert 'supervised_model' not in plan.selection.modules, slug
            if slug == 'api-sin-ui':
                assert not {'ui-planning','figma-handoff','visual-qa'} & {c['id'] for c in plan.selection.capabilities}
            assert plan.selection == resolve(profile,catalog,inventory).selection
            target = root/slug
            compile_project(confirm_plan(plan,True),target,False)
            initial_result = validate_gate(load_project(target)).status
            assert initial_result != 'PASS'
            # Outputs y aprobaciones son ficticios y están marcados; nunca datos de cliente.
            for gate in plan.selection.gates:
                for relative in gate['artifacts']:
                    path = target/relative
                    fields = gate['required_fields'].get(relative,[])
                    if fields:
                        values = read_yaml(path)
                        values.update({field:'SIMULACIÓN — evidencia ficticia' for field in fields})
                        path.write_bytes(write_yaml_bytes(values))
                    else:
                        path.write_text('# SIMULACIÓN\nEvidencia ficticia; sin validación de negocio.\n',encoding='utf-8')
            view = load_project(target)
            assert validate_gate(view).status == 'NEEDS_REVIEW'
            state = view.state.model_dump()
            state['status'] = 'IN_PROGRESS'
            state['gate_reviews'] = {g['id']:{'decision':'PASS','reviewer':'SIMULACIÓN — revisor ficticio',
                'evidence':g['artifacts'] or ['context/business_context.md'],
                'profile_sha256':view.manifest.profile_sha256} for g in plan.selection.gates}
            stages = STAGES[STAGES.index(profile.engagement.current_stage):]
            for index, stage in enumerate(stages):
                state['current_stage'] = stage
                state['completed_stages'] = stages[:index]
                (target/'.acos/state.yaml').write_bytes(write_yaml_bytes(state))
                assert validate_gate(load_project(target)).status == 'PASS', (slug,stage)
            state['status'] = 'COMPLETED'
            state['completed_stages'] = stages
            (target/'.acos/state.yaml').write_bytes(write_yaml_bytes(state))
            before = digest_tree(target)
            closed = load_project(target)
            assert validate_gate(closed).status == 'PASS'
            assert project_status(closed)['completed'] == stages
            next_objective(closed)
            assert before == digest_tree(target)
            moved = root/('moved-'+slug)
            shutil.move(target,moved)
            assert validate_gate(load_project(moved)).status == 'PASS'
            # Perfil alterado debe bloquear; restauración debe recuperar el PASS.
            path = moved/'.acos/project-profile.yaml'
            original = path.read_bytes()
            changed = read_yaml(path); changed['project']['name'] += ' alterado'
            path.write_bytes(write_yaml_bytes(changed))
            assert validate_gate(load_project(moved)).status == 'BLOCKED'
            path.write_bytes(original)
            assert validate_gate(load_project(moved)).status == 'PASS'
            results.append({'case':slug,'result':'PASS','modules':plan.selection.modules,
                'skills':[s.name for s in plan.skills], 'partial_capabilities':[g['capability'] for g in plan.selection.gaps],
                'initial_gate':initial_result, 'stages_checked':len(stages),
                'synthetic_closure':'PASS','moved':'PASS','profile_drift':'BLOCKED','read_only':True})
    return {'kind':'simulación sintética del compiler; no evaluación de skills',
        'cases_passed':len(results),'stages_checked':sum(r['stages_checked'] for r in results),
        'foundry_skills_available':len(inventory.skills),'foundry_findings':[f.model_dump() for f in inventory.findings],
        'results':results}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--foundry',type=Path)
    parser.add_argument('--output',type=Path)
    args = parser.parse_args()
    result = run(args.foundry)
    rendered = json.dumps(result,ensure_ascii=False,indent=2)
    if args.output: args.output.write_text(rendered+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in result.items() if k!='results'},ensure_ascii=False))
