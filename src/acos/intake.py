"""Intake adaptativo; datos faltantes permanecen explícitos."""
import re
from collections.abc import Callable
from .contracts import ProjectProfile,ARCHETYPES,STAGES,valid_slug,AcosError
from .classifier import Classification


def optional(value):return value.strip() or None

def split(value):return [x.strip() for x in value.split(',') if x.strip()]


def collect_profile(initial: ProjectProfile | None, ask: Callable[[str],str]) -> ProjectProfile:
    name=ask('Nombre visible del proyecto: ').strip() if initial is None else initial.project.name
    slug=initial.project.slug if initial else re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')[:64]
    try:valid_slug(slug)
    except ValueError:
        slug=ask('Nombre de carpeta inválido. Indica slug (minúsculas, números y guiones): ').strip();valid_slug(slug)
    if initial is None and slug!=name:
        if ask(f'Carpeta propuesta {slug}. ¿Aceptar? [s/N]: ').lower() not in ('s','si','sí','y','yes'):raise AcosError(130,'Nombre no confirmado.')
    values=ask('Contexto opcional: cliente | industria | mercado | rol (vacío permite cliente confidencial): ').split('|')
    context=dict(zip(['client','industry','market','role'],[optional(v) for v in values]))
    decision=optional(ask('¿Qué decisión necesita tomar el cliente?: '))
    problem=optional(ask('¿Qué problema u oportunidad motiva el trabajo?: '))
    success=optional(ask('¿Cómo se mediría éxito?: '))
    people=ask('¿Quién decide y quién usa el resultado? owner | usuarios: ').split('|')
    declared=ask('Arquetipos '+', '.join(ARCHETYPES)+'; formas analysis/research/automation/product/software/production (arquetipos;formas): ').split(';')
    archetypes=[a.upper() for a in split(declared[0])]
    modes=split(declared[1]) if len(declared)>1 else ['analysis']
    sources=split(ask('Datos existentes (csv, excel, parquet, sql, api, documentos; vacío si no hay): ').lower())
    constraints=split(ask('Restricciones operacionales/presupuesto (separadas por coma): '))
    deliverables=split(ask('Entregables (report, decision_memo, executive_deck, business_case, notebook, api...): '))
    stage=ask('Etapa actual '+', '.join(STAGES)+' [discovery]: ').strip() or 'discovery'
    runtimes=split(ask('Runtime codex, claude_code [ambos]: ').lower()) or ['codex','claude_code']
    chars={}
    if sources:
        chars['tabular']=any(x in ['csv','excel','parquet','sql','api','postgresql','bigquery','snowflake'] for x in sources)
        for key,label in [('temporal','¿Hay temporalidad?'),('panel','¿Se repiten entidades en el tiempo?'),('geospatial','¿Hay información geográfica?')]:
            response=ask(label+' [s/n/desconocido]: ').lower()
            if response in ('s','si','sí','y'):chars[key]=True
            elif response=='n':chars[key]=False
    if 'PREDICT' in archetypes:
        chars['ml_task']=ask('Tarea predictiva (classification/regression/ranking/forecasting/desconocida): ').strip()
        chars['labeled']=ask('Labels (yes/partial/no/unknown): ').strip() or 'unknown'
        chars['supervised']=chars['ml_task'] in ['classification','regression','ranking']
        target=ask('Target/label y momento de disponibilidad (vacío si falta): ').strip()
        if target:chars['target']=target
        if chars['supervised']:
            chars['feature_design']=ask('¿Se requiere diseñar features? [s/N]: ').lower() in ('s','si','sí')
    if 'EXPERIMENT_CAUSAL' in archetypes:
        chars['assignment']=ask('Asignación/intervención disponible (randomized/observational/none/unknown): ').strip() or 'unknown'
    if any(x in modes for x in ['product','software','automation']):
        chars['genai']=ask('¿La solución requiere GenAI? [s/N]: ').lower() in ('s','si','sí')
        chars['ui_required']=ask('¿Requiere interacción UI nueva/modificada? [s/N]: ').lower() in ('s','si','sí')
        if chars['ui_required']:
            for key,label in [('figma','¿Hay Figma?'),('design_system','¿Hay Design System?'),('implemented_ui','¿Hay UI implementada?'),('orca','¿Hay Orca para visual QA?')]:
                chars[key]=ask(label+' [s/N]: ').lower() in ('s','si','sí')
            chars['stack']=ask('Stack (react-shadcn u otro): ').strip()
    unanswered=[]
    for key,value in [('decision',decision),('problem',problem),('success_metric',success),('decision_owner',optional(people[0]))]:
        if value is None:unanswered.append('Confirmar '+key)
    return ProjectProfile(project={'slug':slug,'name':name,**context},engagement={'decision':decision,'problem':problem,'success_metric':success,'decision_owner':optional(people[0]),'users':optional(people[1]) if len(people)>1 else None,'archetypes':archetypes,'delivery_modes':modes,'current_stage':stage,'open_questions':unanswered},data={'sources':sources,'characteristics':chars},constraints=constraints,deliverables=deliverables,runtimes=runtimes)


def review_classification(profile: ProjectProfile, classification: Classification, ask: Callable[[str],str]) -> ProjectProfile:
    choice=ask('Confirma clasificación/perfil [s], corrige arquetipos separados por coma, o cancela [n]: ').strip().lower()
    if choice in ('n','no',''):raise AcosError(130,'Perfil no confirmado.')
    updated=profile.model_dump()
    if choice in ('s','si','sí','y','yes'):
        updated['engagement']['archetypes']=list(dict.fromkeys(classification.archetypes+[p['archetype'] for p in classification.proposals if p['certainty']=='suggested']))
    else:updated['engagement']['archetypes']=[x.upper() for x in split(choice)]
    return ProjectProfile.model_validate(updated)
