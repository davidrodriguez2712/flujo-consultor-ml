"""Comprobaciones locales de runtimes: no inicia turns ni llama a modelos."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import queue
import shutil
import struct
import subprocess
import threading
import tempfile


def skills_probe(codex, cwd):
    proc = subprocess.Popen([str(codex), 'app-server', '--stdio'], cwd=cwd,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding='utf-8')
    messages = queue.Queue()
    def reader():
        for line in proc.stdout:
            try: messages.put(json.loads(line))
            except ValueError: pass
    threading.Thread(target=reader, daemon=True).start()
    threading.Thread(target=lambda: proc.stderr.read(), daemon=True).start()
    def request(method, params, identifier):
        proc.stdin.write(json.dumps({'id': identifier, 'method': method, 'params': params}) + '\n')
        proc.stdin.flush()
        while True:
            response = messages.get(timeout=45)
            if response.get('id') == identifier:
                if 'error' in response: raise RuntimeError(str(response['error']))
                return response['result']
    try:
        init = request('initialize', {'clientInfo': {'name': 'acos_ci_probe', 'version': '0.1.0'}, 'capabilities': {'experimentalApi': True}}, 1)
        proc.stdin.write('{"method":"initialized","params":{}}\n');proc.stdin.flush()
        result = request('skills/list', {'cwds': [str(cwd)], 'forceReload': True}, 2)
        found = [skill for row in result['data'] for skill in row['skills'] if skill['name'] == 'acos-ci-probe']
        if len(found) != 1 or not Path(found[0]['path']).resolve().is_relative_to(cwd.resolve()):
            raise RuntimeError('Codex no descubrió la skill local en el workspace esperado.')
        return {'skill': found[0], 'initialize': init}
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill();proc.wait()


def claude_skills_probe(claude, cwd):
    env = os.environ.copy()
    env['CLAUDE_CONFIG_DIR'] = str(cwd.parent/'isolated-claude-config')
    for key in ['ANTHROPIC_API_KEY','CLAUDE_CODE_OAUTH_TOKEN']:
        env.pop(key, None)
    proc = subprocess.Popen([str(claude), '--print', '--input-format', 'stream-json',
                             '--output-format', 'stream-json', '--verbose',
                             '--setting-sources', 'project', '--strict-mcp-config',
                             '--mcp-config', '{"mcpServers":{}}', '--no-session-persistence'],
                            cwd=cwd, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, encoding='utf-8')
    messages = queue.Queue()
    def reader():
        for line in proc.stdout:
            try: messages.put(json.loads(line))
            except ValueError: pass
    threading.Thread(target=reader, daemon=True).start()
    threading.Thread(target=lambda: proc.stderr.read(), daemon=True).start()
    try:
        # Solo initialize: ningún mensaje user ni petición de generación.
        proc.stdin.write(json.dumps({'type':'control_request','request_id':'acos-init',
                                    'request':{'subtype':'initialize','hooks':None}})+'\n')
        proc.stdin.flush()
        while True:
            response = messages.get(timeout=45)
            if response.get('type') != 'control_response': continue
            data = response['response']
            if data.get('request_id') != 'acos-init': continue
            if data.get('subtype') != 'success': raise RuntimeError('Initialize Claude falló.')
            found = [x for x in data['response']['commands'] if x['name'] == 'acos-ci-probe']
            if len(found) != 1: raise RuntimeError('Claude no descubrió la skill local.')
            return {'command':found[0], 'protocol':'SDK initialize', 'user_messages':0}
    finally:
        proc.terminate()
        try: proc.wait(timeout=10)
        except subprocess.TimeoutExpired: proc.kill();proc.wait()


def pe_machine(path):
    with path.open('rb') as handle:
        if handle.read(2) != b'MZ': raise ValueError('No es un executable PE')
        handle.seek(60); offset = struct.unpack('<I', handle.read(4))[0]
        handle.seek(offset)
        if handle.read(4) != b'PE\x00\x00': raise ValueError('Firma PE inválida')
        return {0x8664: 'x64', 0xaa64: 'arm64'}.get(struct.unpack('<H', handle.read(2))[0], 'other')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--codex', type=Path, required=True)
    parser.add_argument('--claude', type=Path, required=True)
    parser.add_argument('--npm-prefix', type=Path, required=True)
    parser.add_argument('--architecture', choices=['x64', 'arm64'], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args();args.output.mkdir(parents=True, exist_ok=False)
    report = {'platform': platform.platform(), 'python_machine': platform.machine(),
              'expected_architecture': args.architecture, 'model_turns': 0, 'passed': False,
              'checks': [], 'claude_skill_invocation': 'NOT_TESTED_REQUIRES_AUTH',
              'conversation_and_continuity': 'NOT_TESTED_REQUIRES_AUTH'}
    def command(argv, cwd, expected=0):
        result = subprocess.run([str(x) for x in argv], cwd=cwd, capture_output=True,
                                text=True, encoding='utf-8', timeout=60)
        report['checks'].append({'argv': [str(x) for x in argv], 'exit_code': result.returncode,
                                 'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode != expected: raise RuntimeError(f'Exit inesperado: {argv}')
        return result
    try:
        expected_machine = 'arm64' if args.architecture == 'arm64' else 'amd64'
        if platform.machine().lower() != expected_machine: raise RuntimeError('Python no coincide con arquitectura del runner.')
        report['binaries'] = []
        for name in ['codex.exe', 'claude.exe']:
            matches = list(args.npm_prefix.rglob(name))
            if not matches: raise RuntimeError('Falta binary nativo: ' + name)
            for path in matches:
                machine = pe_machine(path)
                report['binaries'].append({'path': str(path), 'machine': machine,
                                          'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
            selected = next((p for p in matches if pe_machine(p) == args.architecture), None)
            if selected is None:
                raise RuntimeError('No existe binary de arquitectura requerida: ' + name)
            setattr(args, 'codex' if name == 'codex.exe' else 'claude', selected.resolve())
        with tempfile.TemporaryDirectory(prefix='acos runtime probe ') as temp:
            workspace = Path(temp) / 'project';workspace.mkdir()
            for runtime in [args.codex, args.claude]:
                command([runtime, '--version'], workspace);command([runtime, '--help'], workspace)
            command([args.claude, 'auth', 'status'], workspace, expected=1)
            command([args.codex, 'login', 'status'], workspace, expected=1)
            from acos.foundry import scan_foundry
            from acos.catalog import load_catalog
            from acos.contracts import ProjectProfile
            from acos.compiler import compile_project
            from acos.resolver import resolve, confirm_plan
            profile = ProjectProfile(project={'slug': 'probe', 'name': 'Probe sintético'}, engagement={'decision': 'Revisar fuentes sintéticas'}, runtimes=['codex','claude_code'])
            project = workspace / 'probe'
            compile_project(confirm_plan(resolve(profile, load_catalog(), scan_foundry(None)), True), project, False)
            # Fixture desechable del harness, no capacidad creada/promovida en Foundry.
            for folder in ['.agents/skills/acos-ci-probe', '.claude/skills/acos-ci-probe']:
                p = project / folder;p.mkdir(parents=True)
                (p/'SKILL.md').write_text('---\nname: acos-ci-probe\ndescription: Fixture sintético de descubrimiento, no usar para consultoría.\n---\n# Fixture\nMarcador ACOS_NATIVE_DISCOVERY.\n', encoding='utf-8')
            report['codex_before_move'] = skills_probe(args.codex, project)
            report['claude_before_move'] = claude_skills_probe(args.claude, project)
            moved = workspace / 'moved project';shutil.move(project, moved)
            report['codex_after_move'] = skills_probe(args.codex, moved)
            report['claude_after_move'] = claude_skills_probe(args.claude, moved)
            report['skill_discovery'] = 'PASS_BOTH_RUNTIMES_BEFORE_AND_AFTER_MOVE'
            report['passed'] = True
    except Exception as exc:
        report['error'] = str(exc);raise
    finally:
        (args.output/'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


if __name__ == '__main__': main()
