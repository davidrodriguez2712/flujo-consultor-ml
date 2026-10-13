"""Recorrido del executable instalado; conserva evidencia incluso ante fallo."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import tempfile
import venv


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--wheel', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    wheel = args.wheel.resolve()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    report = {'platform': platform.platform(), 'machine': platform.machine(),
              'python': sys.version, 'wheel_sha256': hashlib.sha256(wheel.read_bytes()).hexdigest(),
              'commands': [], 'passed': False,
              'scope': 'CLI instalada sin Foundry ni runtimes LLM; no evaluación de eficacia de skills.'}
    env = os.environ.copy()
    env.pop('PYTHONPATH', None)
    env['PYTHONUTF8'] = '1'

    def run(argv, cwd, expected=0, stdin=None):
        result = subprocess.run([str(x) for x in argv], cwd=cwd, env=env,
                                input=stdin, text=True, encoding='utf-8',
                                capture_output=True, timeout=180)
        report['commands'].append({'argv': [str(x) for x in argv],
                                   'expected_exit_code': expected, 'exit_code': result.returncode,
                                   'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode != expected:
            raise RuntimeError(f'Exit {result.returncode}, esperado {expected}: {argv}')
        return result

    try:
        with tempfile.TemporaryDirectory(prefix='acos installed smoke ') as temp:
            sandbox = Path(temp)
            tool = sandbox / 'tool'
            venv.EnvBuilder(with_pip=True).create(tool)
            binaries = tool / ('Scripts' if os.name == 'nt' else 'bin')
            python = binaries / ('python.exe' if os.name == 'nt' else 'python')
            executable = binaries / ('acos.exe' if os.name == 'nt' else 'acos')
            run([python, '-m', 'pip', 'install', str(wheel)], sandbox)
            run([executable, '--version'], sandbox)
            run([python, '-c', 'import acos,sys; from pathlib import Path; assert sys.prefix != sys.base_prefix; assert Path(acos.__file__).resolve().is_relative_to(Path(sys.prefix).resolve()); print(acos.__file__)'], sandbox)
            origin = sandbox / 'origin with spaces'
            origin.mkdir()
            profile = origin / 'profile.yaml'
            profile.write_text('schema_version: 1\nproject:\n  slug: research\n  name: Research\nengagement:\n  archetypes: [DIAGNOSE]\n  delivery_modes: [research]\n  decision: Evaluar entrada a un mercado\ndeliverables: [executive_deck]\nruntimes: [codex, claude_code]\n', encoding='utf-8')
            run([executable, 'init', '--profile-file', profile], origin, stdin='\ns\ns\n')
            project = origin / 'research'
            for command, code in [('status', 0), ('next', 0), ('validate', 3)]:
                response = run([executable, command], project, code)
                data = json.loads(response.stdout)
                if command == 'validate':
                    if data['status'] != 'NEEDS_REVIEW':
                        raise RuntimeError('Discovery debe requerir revisión humana.')
                elif data['integrity'] != 'OK':
                    raise RuntimeError('Integridad del workspace inválida.')
            moved = sandbox / 'moved with spaces'
            shutil.move(project, moved)
            for command, code in [('status', 0), ('next', 0), ('validate', 3)]:
                run([executable, command], moved, code)
            here = sandbox / 'here'
            here.mkdir()
            (here / 'unrelated.txt').write_text('conservar', encoding='utf-8')
            run([executable, 'init', '--here', '--profile-file', profile], here, stdin='\ns\ns\n')
            if (here / 'unrelated.txt').read_text(encoding='utf-8') != 'conservar':
                raise RuntimeError('Se modificó el archivo ajeno.')
            collision = sandbox / 'collision'
            collision.mkdir()
            (collision / 'MANUAL.md').write_text('conservar', encoding='utf-8')
            run([executable, 'init', '--here', '--profile-file', profile], collision, 4, '\ns\ns\n')
            if (collision / 'MANUAL.md').read_text(encoding='utf-8') != 'conservar' or (collision / '.acos').exists():
                raise RuntimeError('Colisión produjo escritura inesperada.')
            report['passed'] = True
    except Exception as exc:
        report['error'] = str(exc)
        raise
    finally:
        (output / 'results.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


if __name__ == '__main__':
    main()
