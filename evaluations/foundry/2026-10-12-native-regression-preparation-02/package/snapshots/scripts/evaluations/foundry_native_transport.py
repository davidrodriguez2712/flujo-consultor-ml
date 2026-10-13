"""Transporte Foundry opt-in. Importar no hace llamadas ni carga credenciales."""
from datetime import date, datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import re
import yaml

MODEL = 'claude-haiku-5-5'
SKILL = 'acos-eval:detect-leakage'
SYSTEM = 'Responde en español. Audita solo el expediente público, respeta sus límites y no aceptes gates. Usa únicamente herramientas y capacidades disponibles. Entrega el reporte y su ruta según case.md.'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class DuplicateReportKey(ValueError):
    pass


class ReportLoader(yaml.SafeLoader):
    """Campos duplicados no pueden ocultarse detrás del último valor YAML."""
    def construct_mapping(self, node, deep=False):
        result = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=deep)
            if key in result:
                raise DuplicateReportKey('frontmatter:duplicate')
            result[key] = self.construct_object(value_node, deep=deep)
        return result


def report_headings(body):
    """ATX del contrato, excluyendo ejemplos fenced y comentarios HTML."""
    headings, fence, comment = [], None, False
    for line in body.splitlines():
        if fence:
            if re.fullmatch(r' {0,3}' + re.escape(fence[0]) + '{' + str(fence[1]) + r',}\s*', line):
                fence = None
            continue
        visible = ''
        while line:
            if comment:
                end = line.find('-->')
                if end < 0: break
                line, comment = line[end+3:], False
            else:
                start = line.find('<!--')
                if start < 0:
                    visible += line
                    break
                visible += line[:start]
                line, comment = line[start+4:], True
        opener = re.match(r'^ {0,3}(`{3,}|~{3,})', visible)
        if opener:
            fence = (opener[1][0], len(opener[1]))
            continue
        heading = re.fullmatch(r' {0,3}#{1,6}\s+(.+?)\s*#*\s*', visible)
        if heading: headings.append(heading[1])
    return headings


def check_report_contract(root, report, final_text, *, report_word_limit=700):
    """Checks mecánicos readonly. No juzga hallazgos, fechas reales o producción."""
    root, report = Path(root), Path(report)
    result = {'success': False, 'errors': [], 'report_words': None, 'final_words': None,
              'report_word_limit': report_word_limit, 'final_word_limit': 80,
              'semantic_review': 'REQUIRED'}
    errors = result['errors']
    if not isinstance(final_text, str) or not final_text.strip():
        errors.append('final:missing')
    else:
        result['final_words'] = len(final_text.split())
        if result['final_words'] > 80: errors.append('final:word_limit')
    if not report.is_file() or report.is_symlink():
        errors.append('report:missing')
        return result
    try:
        text = report.read_text(encoding='utf-8')
        result['report_words'] = len(text.split())
        if result['report_words'] > report_word_limit: errors.append('report:word_limit')
        match = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)', text, re.S)
        if not match:
            errors.append('frontmatter:missing')
            return result
        try:
            meta = yaml.load(match[1], Loader=ReportLoader)
        except DuplicateReportKey:
            errors.append('frontmatter:duplicate')
            return result
        except (ValueError, yaml.YAMLError):
            errors.append('frontmatter:invalid')
            return result
        if not isinstance(meta, dict):
            errors.append('frontmatter:invalid')
            return result
        for key in ['skill', 'version', 'fecha', 'inputs', 'estado', 'condicion']:
            if key not in meta: errors.append('missing:' + key)
        context = json.loads((root/'.runtime/report-context.json').read_text())
        for key in ['skill', 'version', 'condicion']:
            if key in meta and meta[key] != context[key]: errors.append('context:' + key)
        if not isinstance(meta.get('estado'), str) or not meta['estado'].strip():
            errors.append('value:estado')
        try:
            value = meta.get('fecha')
            if isinstance(value, str): value = datetime.fromisoformat(value)
            if not isinstance(value, (date, datetime)): raise ValueError('Fecha inválida')
        except ValueError:
            errors.append('value:fecha')
        sources = [root/'case.md', root/'inputs']
        if any(p.is_symlink() for path in sources for p in [path, *path.parents]):
            errors.append('inputs:unsafe')
            return result
        if not (root/'case.md').is_file():
            errors.append('inputs:coverage')
            return result
        expected = {}
        for path in [root/'case.md', *sorted((root/'inputs').rglob('*'))]:
            if any(p.is_symlink() for p in [path, *path.parents]):
                errors.append('inputs:unsafe')
                return result
            if path.is_file(): expected[str(path.relative_to(root))] = digest(path)
        observed = {}
        rows = meta.get('inputs')
        if not isinstance(rows, list): rows = []
        for row in rows:
            if isinstance(row, str):
                legacy = re.fullmatch(r'(\S+) sha256 ([a-f0-9]{64})(?: \(\d+ filas\))?', row)
                row = {'path': legacy[1], 'sha256': legacy[2]} if legacy else {}
            if not isinstance(row, dict) or not isinstance(row.get('path'), str):
                errors.append('inputs:hash')
                continue
            path, value = row['path'], row.get('sha256')
            if path in observed or path not in expected or value != expected.get(path):
                errors.append('inputs:hash')
            observed[path] = value
        if set(observed) != set(expected): errors.append('inputs:coverage')
        headings = report_headings(text[match.end():])
        for title in ['Resumen', 'Hallazgos', 'Evidencia', 'Preguntas abiertas', 'Recomendaciones']:
            if headings.count(title) != 1: errors.append('section:' + title)
    except (OSError, UnicodeError, yaml.YAMLError, TypeError, KeyError, ValueError):
        errors.append('contract:unreadable')
    result['errors'] = list(dict.fromkeys(errors))
    result['success'] = not result['errors']
    return result


class ToolCallRejected(ValueError):
    def __init__(self, reason, name, args):
        super().__init__(reason)
        self.tool_name, self.tool_input = name, args


class ToolPolicy:
    """Valida inputs de herramientas antes de entregar tool_use al CLI."""
    def __init__(self, root, readable, report, command, skill):
        self.root = Path(root).resolve()
        self.readable = {self.root / p for p in readable}
        self.report = Path(report).resolve()
        if not self.report.is_relative_to(self.root) or self.report.exists():
            raise ValueError('Reporte fuera de workspace o existente')
        self.command, self.skill = command, skill
        self.hashes = {p: digest(p) for p in self.readable}
        self.write_claimed = False
        self.tool_calls = []

    def verify_inputs(self):
        for path, expected in self.hashes.items():
            if any(p.is_symlink() for p in [path, *path.parents]) or digest(path) != expected:
                raise ValueError('Input alterado o symlink')

    def validate_tool_call(self, name, args):
        try:
            self._validate_tool_call(name,args)
        except ValueError as exc:
            raise ToolCallRejected(str(exc),name,args) from exc

    def _validate_tool_call(self, name, args):
        self.verify_inputs()
        if not isinstance(args, dict):
            raise ValueError('Input de herramienta inválido')
        if name in {'Read', 'Write'}:
            raw = args.get('file_path')
            if not isinstance(raw, str): raise ValueError('Ruta ausente')
            path = Path(raw)
            if not path.is_absolute(): path = self.root / path
            if any(p.is_symlink() for p in [path, *path.parents]):
                raise ValueError('Ruta symlink')
            path = path.resolve()
            if name == 'Read' and path not in self.readable:
                raise ValueError('Lectura fuera de inputs permitidos')
            if name == 'Write':
                if path != self.report or path.exists() or self.write_claimed:
                    raise ValueError('Escritura fuera de reporte nuevo')
                if not isinstance(args.get('content'), str) or len(args['content'].encode()) > 512_000:
                    raise ValueError('Contenido de reporte inválido')
                self.write_claimed = True
        elif name == 'Bash':
            if args.get('command') != self.command or args.get('run_in_background'):
                raise ValueError('Comando no permitido')
        elif name == 'Skill':
            if not self.skill or args.get('skill') != self.skill:
                raise ValueError('Skill no permitida')
        else:
            raise ValueError('Herramienta no permitida')
        self.tool_calls.append({'name': name, 'input': args})


def validate_provider_tools(events, policy):
    """Reconstruye JSON fragmentado; no permite ejecución con fragmentos sin validar."""
    pending = {}
    for event in events:
        kind, index = event.get('type'), event.get('index')
        if kind == 'content_block_start':
            block = event.get('content_block', {})
            if block.get('type') == 'tool_use':
                if index in pending: raise ValueError('Bloque duplicado')
                pending[index] = [block.get('name'), block.get('input'), '']
            elif block.get('type') not in {'text', 'thinking', 'redacted_thinking'}:
                raise ValueError('Bloque remoto/no soportado')
        elif kind == 'content_block_delta' and event.get('delta', {}).get('type') == 'input_json_delta':
            if index not in pending: raise ValueError('Delta sin herramienta')
            fragment = event['delta'].get('partial_json')
            if not isinstance(fragment, str): raise ValueError('JSON de herramienta inválido')
            pending[index][2] += fragment
        elif kind == 'content_block_stop' and index in pending:
            name, initial, fragments = pending.pop(index)
            if fragments and initial not in ({}, None): raise ValueError('Input duplicado')
            args = json.loads(fragments) if fragments else initial
            policy.validate_tool_call(name, args)
    if pending: raise ValueError('Herramienta truncada')


def stage_workspace(case, workspace, skill=None, *, workflow=None):
    case, root = Path(case), Path(workspace)
    sources = [case/'case.md', *sorted((case/'inputs').rglob('*'))]
    if not (case/'inputs').is_dir(): raise ValueError('Inputs ausentes')
    if any(p.is_symlink() for p in sources): raise ValueError('Fuente symlink')
    root.mkdir(parents=True, exist_ok=False)
    for source in sources:
        if source.is_file():
            target = root/source.relative_to(case);target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
    (root/'reports/leakage').mkdir(parents=True)
    runtime = root/'.runtime';runtime.mkdir()
    shutil.copyfile(Path(__file__).with_name('foundry_input_facts.py'), runtime/'check_inputs.py')
    if workflow:
        shutil.copyfile(workflow,root/'workflow.md')
        if digest(root/'workflow.md')!=digest(Path(workflow)):raise ValueError('Workflow snapshot distinto')
    plugin = None
    context={'condicion':'baseline','skill':'none','version':None,'skill_sha256':None}
    if skill:
        raw=Path(skill).read_text()
        if not raw.startswith('---\n'):raise ValueError('Skill sin metadata')
        meta=yaml.safe_load(raw.split('---',2)[1])
        version=meta.get('version') if isinstance(meta,dict) else None
        if not isinstance(meta,dict) or meta.get('name')!='detect-leakage' or not isinstance(version,str) or not re.fullmatch(r'\d+\.\d+\.\d+',version):
            raise ValueError('Skill/name/version inválida')
        plugin = runtime/'plugin';(plugin/'.claude-plugin').mkdir(parents=True)
        (plugin/'.claude-plugin/plugin.json').write_text(json.dumps({'name':'acos-eval','version':version}))
        dest=plugin/'skills/detect-leakage/SKILL.md';dest.parent.mkdir(parents=True)
        shutil.copyfile(skill,dest)
        if digest(dest)!=digest(Path(skill)): raise ValueError('Snapshot de skill distinto')
        context.update(condicion='treatment',skill='detect-leakage',version=version,skill_sha256=digest(dest))
    (runtime/'report-context.json').write_text(json.dumps(context,ensure_ascii=False,indent=2)+'\n')
    return plugin


def invoke(case, output, proxy, cli, *, skill=None, workflow=None, max_requests=8, timeout=240, report_word_limit=700):
    """Usa proxy ya autorizado por coordinador; no lee claves ni aprueba presupuesto."""
    if type(report_word_limit) is not int or not 1<=report_word_limit<=700:raise ValueError('Límite de extensión inválido')
    target=Path(output);target.mkdir(parents=True,exist_ok=False)
    root=target/'workspace';plugin=stage_workspace(case,root,skill,workflow=workflow)
    root=root.resolve(); report=root/'reports/leakage/audit.md'
    readable={'case.md','.runtime/check_inputs.py','.runtime/report-context.json',*[str(p.relative_to(root)) for p in (root/'inputs').rglob('*') if p.is_file()]}
    if workflow:readable.add('workflow.md')
    if plugin:
        readable.add(str((plugin/'skills/detect-leakage/SKILL.md').relative_to(root)))
        readable.add(str((plugin/'.claude-plugin/plugin.json').relative_to(root)))
    command=shlex.join([sys.executable,str(root/'.runtime/check_inputs.py')])
    policy=ToolPolicy(root,readable,report,command,SKILL if plugin else None)
    start=len(proxy.budget.entries);global_limit=proxy.budget.max_requests
    if not 1<=max_requests<=8 or start>=global_limit:raise ValueError('Límite de solicitudes')
    proxy.budget.max_requests=min(global_limit,start+max_requests)
    policy.request_start=start
    proxy.local_tool_policy=policy
    config=target/'isolated-config';config.mkdir()
    allow=[*[f'Read(/{root/p})' for p in sorted(readable)],f'Edit(/{report})',f'Bash({command})',f'Skill({SKILL})']
    deny=['Agent','WebFetch','WebSearch','NotebookEdit',f'Edit(/{root}/inputs/**)',f'Edit(/{root}/case.md)',f'Edit(/{root}/.runtime/**)']
    settings=json.dumps({'disableBundledSkills':True,'permissions':{'allow':allow,'deny':deny}})
    argv=[str(cli),'-p','--restricted','--no-chrome','--no-session-persistence',
          '--setting-sources','','--settings',settings,'--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
          '--permission-mode','dontAsk','--permission-prompts','none','--tools','Read,Write,Bash,Skill',
          '--max-turns',str(max_requests),'--effort','low','--model',MODEL,'--system-prompt',SYSTEM,
          '--output-format','stream-json','--verbose']
    if plugin:argv += ['--plugin-dir',str(plugin)]
    env={k:v for k,v in os.environ.items() if k in {'PATH','HOME','TMPDIR','LANG','LC_ALL','SYSTEMROOT'}}
    env.update(CLAUDE_CONFIG_DIR=str(config.resolve()),ANTHROPIC_API_KEY='local-proxy-placeholder',
               ANTHROPIC_BASE_URL=proxy.url,CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1',ANTHROPIC_MAX_RETRIES='0')
    prompt='Lee case.md y audita únicamente sus inputs autorizados. Cumple el contrato común; utiliza solo capacidades disponibles y pertinentes. Entrega resumen y ruta de reporte.'
    if workflow:prompt='Lee workflow.md y sigue sus pautas. '+prompt
    prompt+='\nLee .runtime/report-context.json: suministra metadatos conocidos de condición y versión; no contiene conclusiones de auditoría. Úsalo para los campos que solicite el contrato.\n'
    prompt+=f'\nLa auditoría se limita al expediente: escribe un reporte de máximo {report_word_limit} palabras, sin omitir el contrato ni evidencia esencial. No reproduzcas las instrucciones ni el reporte completo en la respuesta final; entrega un resumen de máximo 80 palabras y la ruta. Revisa solo familias aplicables y declara límites, sin desarrollar análisis ajenos al encargo.\n'
    prompt+='\nContrato mecánico del reporte: frontmatter YAML al inicio físico del archivo, sin fences exteriores, con claves exactas skill, version, fecha, inputs, estado, condicion; sin claves duplicadas. Copia skill/version/condicion de report-context. fecha en ISO corresponde a la ejecución real; estado describe la auditoría, no aprobación de gates. inputs enumera case.md y todos los archivos de inputs con path y sha256 de la utility. Después incluye una vez cada sección: Resumen, Hallazgos, Evidencia, Preguntas abiertas, Recomendaciones. El conteo usa whitespace en todo el archivo, incluido frontmatter; las 80 palabras finales incluyen la ruta. El cumplimiento mecánico se comprueba por separado y no sustituye revisión semántica.\n'
    prompt+='\n\nContrato operativo de herramientas:\n'
    prompt+='Read: únicamente estos archivos:\n'+'\n'.join(str(root/p) for p in sorted(readable))+'\n'
    prompt+=f'Write: únicamente un reporte nuevo en {report}. No modificar inputs ni crear otros archivos.\n'
    prompt+='Bash: solo este comando exacto, sin prefijos, sufijos, argumentos adicionales ni comandos encadenados:\n'+command+'\n'
    prompt+='La utility produce hashes, tamaños y conteos de CSV; no ejecuta pipeline.py ni evalúa leakage. No usar ls, pwd, cat, shell arbitrario, red ni instalar paquetes.\n'
    prompt+='Skill: solo acos-eval:detect-leakage. Si está instalada, invócala al inicio mediante Skill antes de auditar. Si está ausente, realiza la tarea sin skill y declara none/null. No invocar skills ausentes ni subagents.\n'
    metadata={'started_at':datetime.now(timezone.utc).isoformat(),'argv':argv,'runtime_success':False,
              'condition':'treatment' if plugin else 'baseline','skill_invoked':False,'request_count':0}
    (target/'prompt.txt').write_text(prompt.replace(proxy.key,'[REDACTED]'),encoding='utf-8')
    metadata['prompt_sha256']=digest(target/'prompt.txt')
    try:
        result=subprocess.run(argv,input=prompt,text=True,encoding='utf-8',capture_output=True,cwd=root,env=env,timeout=timeout,check=False)
        stdout,stderr,code=result.stdout,result.stderr,result.returncode
    except subprocess.TimeoutExpired as exc:
        def decode(value):return value.decode('utf-8',errors='replace') if isinstance(value,bytes) else value or ''
        stdout,stderr,code=decode(exc.stdout),decode(exc.stderr),None;metadata['error']='timeout'
    except OSError:
        stdout,stderr,code='','',None;metadata['error']='native-launch-failed'
    stdout=stdout.replace(proxy.key,'[REDACTED]');stderr=stderr.replace(proxy.key,'[REDACTED]')
    (target/'stdout.jsonl').write_text(stdout);(target/'stderr.txt').write_text(stderr)
    entries=proxy.budget.entries[start:];metadata.update(returncode=code,request_count=len(entries),tool_calls=policy.tool_calls)
    metadata['skill_invoked']=any(x['name']=='Skill' and x['input'].get('skill')==SKILL for x in policy.tool_calls)
    final=None
    try:
        messages=[json.loads(line) for line in stdout.splitlines() if line.strip()]
        finals=[x for x in messages if x.get('type')=='result']
        if len(finals)==1:final=finals[0]
        metadata['skill_invocation_requested']=metadata['skill_invoked']
        metadata['skill_invoked']=any(x.get('type')=='user' and x.get('tool_use_result',{}).get('success') is True and x.get('tool_use_result',{}).get('commandName')==SKILL for x in messages)
        policy.verify_inputs()
        models=(final or {}).get('modelUsage',{})
        known=bool(entries) and all(e.get('estimated_usd') is not None for e in entries)
        healthy=known and all(e.get('http_status')==200 and e.get('provider_stop_reason') in {'tool_use','end_turn'} and not any(e.get(k) for k in ['bound_exceeded','transport_error','tool_guard_error']) for e in entries)
        metadata['runtime_success']=(code==0 and final is not None and final.get('subtype')=='success' and final.get('is_error') is False and not final.get('permission_denials') and set(models)=={MODEL} and healthy and entries[-1]['provider_stop_reason']=='end_turn' and report.is_file() and (metadata['skill_invoked'] if plugin else not metadata['skill_invocation_requested']))
        metadata.update(usage_known=known,report_persisted=report.is_file(),report_sha256=digest(report) if report.is_file() else None,model_usage=models)
        if final and isinstance(final.get('result'),str):(target/'result.txt').write_text(final['result'])
    except (ValueError,TypeError,OSError,AttributeError):metadata['error']='invalid-output-or-input-integrity'
    contract=check_report_contract(root,report,(final or {}).get('result'),report_word_limit=report_word_limit)
    (target/'report-contract.json').write_text(json.dumps(contract,ensure_ascii=False,indent=2)+'\n')
    metadata['contract_success']=contract['success']
    metadata['execution_success']=metadata['runtime_success'] and metadata['contract_success']
    # No restablecer límites si ocurrió un fallo: evita que otra invocación reactive solicitudes.
    if metadata['execution_success']:
        proxy.budget.max_requests=global_limit
    else:proxy.budget.max_requests=len(proxy.budget.entries)
    metadata['finished_at']=datetime.now(timezone.utc).isoformat()
    (target/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    return metadata
