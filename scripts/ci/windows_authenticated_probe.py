"""Probe autenticado, solo lectura, con presupuesto y evidencias explícitas."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import uuid
import shutil
from contextlib import contextmanager

from runtime_budget import Proxy, MODELS
from windows_runtime_probe import pe_machine


def hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}


def decode_console(raw):
    return (raw or b'').decode('utf-8', errors='replace')


@contextmanager
def readable_workspace(base):
    # Python 3.13 en Windows crea TemporaryDirectory con ACL privadas (0700).
    # El token restringido de Codex no puede leerlas. mkdir hereda las ACL de CI.
    root = base.resolve() / ('acos-probe-' + uuid.uuid4().hex)
    root.mkdir()
    try: yield root
    finally: shutil.rmtree(root)


def fixture(root, skill):
    from acos.catalog import load_catalog
    from acos.compiler import compile_project
    from acos.contracts import ProjectProfile, ProjectState
    from acos.foundry import scan_foundry
    from acos.resolver import resolve, confirm_plan
    from acos.yaml_io import write_yaml_bytes
    profile = ProjectProfile(project={'slug':'churn-probe', 'name':'Churn sintético — runtime Windows'},
        engagement={'decision':'Priorizar retención mensual', 'success_metric':'Margen esperado',
                    'current_stage':'validation', 'archetypes':['PREDICT','PRIORITIZE_SELECT']},
        data={'characteristics': {'temporal':True, 'panel':True}},
        runtimes=['codex', 'claude_code'])
    project = root / 'churn-probe'
    compile_project(confirm_plan(resolve(profile, load_catalog(), scan_foundry(None)), True), project, False)
    marker = 'CHURN-WIN-' + uuid.uuid4().hex[:10]
    state = ProjectState(current_stage='validation', status='BLOCKED',
        objective=marker + ': auditar split temporal y leakage antes de recomendar retención',
        blockers=['Falta confirmar la fecha de disponibilidad de las labels.'])
    (project / '.acos/state.yaml').write_bytes(write_yaml_bytes(state))
    with (project / 'AGENTS.md').open('a', encoding='utf-8') as handle:
        handle.write('\n## Pauta de lectura para este probe en Windows\n\n'
                     'Para exec_command de Codex: especificar login=false y workdir=' + str(project) + '. '
                     'En PowerShell, leer con Get-Content -LiteralPath usando rutas absolutas bajo ' + str(project) + '. '
                     'Se pueden leer varias rutas literales en un solo Get-Content, separadas por comas. '
                     'Evitar cadenas con punto y coma, pipes, interpolación o comandos de escritura. '
                     'La política es de solo lectura. No solicitar permisos adicionales. '
                     'Al resumir continuidad, incluir el identificador exacto del objetivo canónico.\n')
    for folder in ['.agents/skills/design-validation', '.claude/skills/design-validation']:
        path = project / folder; path.mkdir(parents=True)
        (path / 'SKILL.md').write_bytes(skill.read_bytes())
    return project, marker


def evidence(runtime, text, marker, guided):
    events = []
    for line in text.splitlines():
        try: events.append(json.loads(line))
        except ValueError: pass
    replies = []
    tools = []
    successful_results = set()
    for event in events:
        if runtime == 'codex':
            item = event.get('item', {})
            if event.get('type') == 'item.completed' and item.get('type') == 'agent_message':
                replies.append(item.get('text', ''))
            if item.get('type') == 'command_execution':
                tools.append({'tool':'command_execution', 'input':item.get('command', ''),
                              'status':item.get('status'), 'exit_code':item.get('exit_code')})
        elif event.get('type') == 'assistant':
            for item in event.get('message', {}).get('content', []):
                if item.get('type') == 'text': replies.append(item['text'])
                if item.get('type') == 'tool_use':
                    tools.append({'tool':item.get('name'), 'input':item.get('input'), 'id':item.get('id')})
        elif runtime == 'claude' and event.get('type') == 'user':
            content = event.get('message', {}).get('content', [])
            if isinstance(content, list):
                for item in content:
                    if item.get('type') == 'tool_result' and not item.get('is_error', False):
                        successful_results.add(item.get('tool_use_id'))
    reply = '\n'.join(replies)
    low = reply.lower()
    if runtime == 'codex':
        native = any('design-validation' in str(t['input']) and 'SKILL.md' in str(t['input'])
                     and t.get('exit_code') == 0 for t in tools)
    else:
        native = any(t['tool'] == 'Skill' and t['input'].get('skill') == 'design-validation'
                     and t.get('id') in successful_results for t in tools)
    checks = {'canonical_objective': marker in reply,
              'blocked_state': 'blocked' in low or 'bloquead' in low,
              'label_availability': 'label' in low and ('disponib' in low or 'fecha' in low),
              'native_skill_trace': native if guided else None,
              'validation_advice': ('split' in low or 'validaci' in low) if guided else None}
    return {'checks':checks, 'passed':all(v for v in checks.values() if v is not None),
            'reply':reply, 'tools':tools}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--npm-prefix', type=Path, required=True)
    parser.add_argument('--architecture', choices=['x64','arm64'], required=True)
    parser.add_argument('--skill', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--runtime-budget', type=float, default=0.25)
    parser.add_argument('--runtime', choices=['both','codex','claude'], default='both')
    args = parser.parse_args(); args.output.mkdir(parents=True, exist_ok=False)
    if not 0 < args.runtime_budget <= 0.25: raise ValueError('Máximo US$0.25 por runtime y arquitectura.')
    chosen = ['codex','claude'] if args.runtime == 'both' else [args.runtime]
    report = {'platform':platform.platform(), 'architecture':args.architecture, 'requested_runtimes':chosen,
              'scope':'Skill real + continuemos en sesión nueva; solo lectura; sin eficacia ni resume persistido',
              'skill_sha256':hashlib.sha256(args.skill.read_bytes()).hexdigest(),
              'skill_status':'experimental', 'runtime_budget_usd':args.runtime_budget,
              'passed':False, 'runtimes':[]}
    try:
        for runtime in chosen:
            key_name = 'OPENAI_API_KEY' if runtime == 'codex' else 'ANTHROPIC_API_KEY'
            key = os.environ.get(key_name)
            if not key: raise RuntimeError('Secret no disponible: ' + key_name)
            executable = next((p for p in args.npm_prefix.rglob(runtime + '.exe')
                               if pe_machine(p) == args.architecture), None)
            if executable is None: raise RuntimeError('Falta binary nativo: ' + runtime)
            row = {'runtime':runtime, 'model':MODELS[runtime], 'passed':False, 'runs':[],
                   'requests':[], 'committed_usd':0, 'estimated_usd':0, 'unmeasured_requests':0}
            report['runtimes'].append(row)
            with readable_workspace(Path.cwd()) as root, Proxy(runtime, key, args.runtime_budget) as proxy:
                project, marker = fixture(root, args.skill)
                before = hashes(project)
                env = dict(os.environ)
                for name in ['OPENAI_API_KEY','ANTHROPIC_API_KEY','CLAUDE_CODE_OAUTH_TOKEN','GH_TOKEN','GITHUB_TOKEN']:
                    env.pop(name, None)
                # Claves reales permanecen en el proxy, fuera del proceso del agente.
                env.update({'PYTHONUTF8':'1', 'DISABLE_AUTOUPDATER':'1', 'DISABLE_TELEMETRY':'1',
                            'DISABLE_ERROR_REPORTING':'1', 'CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC':'1',
                            'API_MAX_RETRIES':'0', 'CLAUDE_CODE_MAX_OUTPUT_TOKENS':'1024'})
                runtime_home = root / 'runtime-home'; runtime_home.mkdir()
                if runtime == 'codex':
                    env['CODEX_HOME'] = str(runtime_home)
                    env['ACOS_PROXY_TOKEN'] = 'local-probe-only'
                    base = [str(executable),'exec','--ignore-user-config','--ephemeral','--skip-git-repo-check',
                            '--sandbox','read-only','--json','-C',str(project),'-m',MODELS[runtime]]
                    for setting in ['model_provider="acos_probe"', 'model_reasoning_effort="low"', 'web_search="disabled"',
                                    'windows.sandbox="unelevated"',
                                    'model_providers.acos_probe.name="ACOS bounded probe"',
                                    'model_providers.acos_probe.wire_api="responses"',
                                    'model_providers.acos_probe.env_key="ACOS_PROXY_TOKEN"',
                                    'model_providers.acos_probe.base_url="' + proxy.url + '/v1"',
                                    'model_providers.acos_probe.request_max_retries=0',
                                    'model_providers.acos_probe.stream_max_retries=0']:
                        base.extend(['-c',setting])
                    # Verificar filesystem y sandbox sin un turn de modelo.
                    shell = shutil.which('pwsh')
                    if not shell: raise RuntimeError('PowerShell no disponible')
                    preflight = subprocess.run([str(executable),'sandbox',
                        '-c','windows.sandbox="unelevated"','-c','permissions.acos_read.extends=":read-only"',
                        '--permission-profile','acos_read','-C',str(project),'--',shell,
                        '-NoProfile','-Command',"Get-Content -LiteralPath '" + str(project/'.acos/state.yaml') + "'"],
                        cwd=project,env=env,capture_output=True,timeout=45)
                    (args.output/'codex-sandbox-read-stdout.bin').write_bytes(preflight.stdout or b'')
                    (args.output/'codex-sandbox-read-stderr.bin').write_bytes(preflight.stderr or b'')
                    row['sandbox_read_preflight'] = {'exit_code':preflight.returncode,
                        'stdout':decode_console(preflight.stdout),'stderr':decode_console(preflight.stderr),
                        'passed':preflight.returncode == 0 and marker.encode('ascii') in (preflight.stdout or b'')}
                    if not row['sandbox_read_preflight']['passed']:
                        raise RuntimeError('Preflight de lectura falló; no iniciar modelo.')
                else:
                    env['CLAUDE_CONFIG_DIR'] = str(runtime_home)
                    env['ANTHROPIC_API_KEY'] = 'local-probe-only'
                    env['ANTHROPIC_BASE_URL'] = proxy.url
                    git_bash = Path('C:/Program Files/Git/bin/bash.exe')
                    if git_bash.exists(): env['CLAUDE_CODE_GIT_BASH_PATH'] = str(git_bash)
                    base = [str(executable),'-p','--output-format','stream-json','--verbose',
                            '--no-session-persistence','--setting-sources','project',
                            '--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
                            '--tools','Read,Glob,Grep,Skill','--allowedTools','Read,Glob,Grep,Skill',
                            '--permission-mode','dontAsk','--max-turns','10','--max-budget-usd',str(args.runtime_budget),
                            '--model',MODELS[runtime]]
                invocation = ('Usa $design-validation y lee .agents/skills/design-validation/SKILL.md. '
                              if runtime == 'codex' else
                              'Primero usa Read para leer AGENTS.md y .acos/state.yaml. Luego carga las instrucciones '
                              'mediante la herramienta Skill con skill="design-validation". ')
                prompts = [('guided', invocation +
                           'Esta es una prueba de integración de runtime. Verifica las preconditions '
                           'después de cargar las instrucciones. El fixture no contiene dataset ni '
                           'código de entrenamiento, solamente metadata y templates. '
                           'Lee el estado canónico. Informa el objetivo '
                           'con su identificador exacto, etapa, status y bloqueo; aplica la skill a un '
                           'checklist breve de validación temporal. No inventes inputs ni apruebes gates. '
                           'Esta prueba es SOLO LECTURA: no persistas el reporte ni modifiques archivos. '
                           'No ejecutes código ni delegues. Responde en español, máximo 180 palabras.'),
                           ('continuity','continuemos')]
                try:
                    for label, prompt in prompts:
                        proc = subprocess.Popen(base + [prompt], cwd=project, env=env,
                                                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                                text=True, encoding='utf-8')
                        try: stdout, stderr = proc.communicate(timeout=150)
                        except subprocess.TimeoutExpired:
                            proc.kill(); stdout, stderr = proc.communicate()
                            row['error'] = 'timeout; no reintento'
                        # No auth.json, environments ni headers en artifacts.
                        for secret in [key]:
                            stdout = stdout.replace(secret, '[REDACTED]')
                            stderr = stderr.replace(secret, '[REDACTED]')
                        (args.output / (runtime + '-' + label + '.jsonl')).write_text(stdout, encoding='utf-8')
                        (args.output / (runtime + '-' + label + '-stderr.txt')).write_text(stderr, encoding='utf-8')
                        result = evidence(runtime, stdout, marker, label == 'guided')
                        result.update({'test':label, 'exit_code':proc.returncode,
                                       'workspace_unchanged':before == hashes(project)})
                        result['passed'] = result['passed'] and proc.returncode == 0 and result['workspace_unchanged']
                        row['runs'].append(result)
                        if not result['passed']: break
                    row['passed'] = len(row['runs']) == 2 and all(r['passed'] for r in row['runs'])
                finally:
                    row['requests'] = proxy.budget.entries
                    row['rejections'] = proxy.rejections
                    row['committed_usd'] = proxy.budget.committed
                    row['estimated_usd'] = sum(e['estimated_usd'] or 0 for e in proxy.budget.entries)
                    row['unmeasured_requests'] = sum(e['estimated_usd'] is None for e in proxy.budget.entries)
            # Si falla un runtime, no gastar en el siguiente.
            if not row['passed']: break
        report['passed'] = len(report['runtimes']) == len(chosen) and all(r['passed'] for r in report['runtimes'])
    except Exception as exc:
        report['error'] = str(exc)
    finally:
        (args.output/'results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    if not report['passed']: raise SystemExit(1)


if __name__ == '__main__': main()
