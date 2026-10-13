"""Coordinador Foundry; importar/verificar no lee credenciales ni hace llamadas."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import subprocess

SCHEDULE = [('smoke', 'baseline'), ('L01', 'baseline'), ('L01', 'treatment'),
            ('L02', 'treatment'), ('L02', 'baseline'), ('L03', 'baseline'), ('L03', 'treatment')]


def load(path):
    return json.loads(Path(path).read_text())


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def verify(package):
    package = Path(package).resolve()
    manifest = package/'execution-manifest-01.json'
    for row in load(manifest)['files']:
        path = package/row['path']
        if not path.resolve().is_relative_to(package) or path.is_symlink() or sha(path) != row['sha256']:
            raise ValueError('Snapshot alterado o fuera del paquete')
    config = load(package/'config.json')
    if config['schedule'] != [list(x) for x in SCHEDULE] or config['model'] != 'claude-haiku-5-5':
        raise ValueError('Configuración incompatible')
    if config['max_requests'] != 56 or config['per_invocation'] != 8 or type(config['output_cap']) is not int or config['output_cap'] not in {4096,8192} or config['budget_ceiling_usd'] != .10:
        raise ValueError('Límites incompatibles')
    limit=config.get('report_word_limit',700)
    if type(limit) is not int or not 1<=limit<=700:raise ValueError('Límite de extensión inválido')
    return config, sha(manifest)


def require_approval(approval, manifest):
    amount = approval.get('total_budget_usd')
    if (approval.get('status') != 'APPROVED' or approval.get('execution_manifest_sha256') != manifest
        or approval.get('package_accepted') is not True or isinstance(amount, bool)
        or not isinstance(amount, (int, float)) or not 0 < amount <= .10):
        raise ValueError('Falta aceptación del paquete y presupuesto ligado al manifest (máximo US$0.10)')
    return amount


def execute(package, output, proxy, cli, transport, *, report_word_limit=700):
    """Proxy autorizado por main; inyección permite probar sin proveedor real."""
    package, output = Path(package).resolve(), Path(output).resolve()
    output.mkdir(parents=True, exist_ok=False)
    summary = {'status': 'RUNNING', 'runs': [], 'effectiveness': 'NOT_REVIEWED'}
    try:
        for case, condition in SCHEDULE:
            result = transport.invoke(package/'public'/case, output/(case+'-'+condition), proxy, cli,
                skill=package/'skill/SKILL.md' if condition == 'treatment' else None,
                workflow=package/'workflow.md', max_requests=8, timeout=240, report_word_limit=report_word_limit)
            summary['runs'].append({'case': case, 'condition': condition, 'runtime_success': result['runtime_success']})
            (output/'ledger.json').write_text(json.dumps({'entries': proxy.budget.entries, 'rejections': proxy.rejections}, indent=2)+'\n')
            if not result['runtime_success']:
                summary['status'] = 'STOPPED_RUNTIME_FAILURE'
                break
        else:
            summary['status'] = 'COMPLETED_PENDING_CONTENT_REVIEW'
    except Exception:
        summary['status'] = 'STOPPED_COORDINATOR_FAILURE'
        raise
    finally:
        proxy.budget.max_requests = len(proxy.budget.entries)
        (output/'ledger.json').write_text(json.dumps({'entries': proxy.budget.entries, 'rejections': proxy.rejections}, indent=2)+'\n')
        (output/'summary.json').write_text(json.dumps(summary, indent=2)+'\n')
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--package', required=True)
    parser.add_argument('--output')
    parser.add_argument('--approval')
    parser.add_argument('--cli', default='claude')
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    package = Path(args.package).resolve()
    config, manifest = verify(package)
    if args.verify_only:
        print(json.dumps({'status': 'PASS_FROZEN_CONFIG', 'manifest_sha256': manifest, 'paid_calls': 0}))
        return
    if not args.approval or not args.output:
        raise ValueError('Faltan aprobación y output nuevo')
    amount = require_approval(load(args.approval), manifest)
    # Verificar versión antes de leer credenciales o crear proxy.
    version = subprocess.run([args.cli, '--version'], capture_output=True, text=True, timeout=30, check=True).stdout.strip()
    if version != config['cli_version']:
        raise ValueError('Versión CLI distinta; revisar/configurar de nuevo')
    if Path(args.output).exists():
        raise ValueError('Output ya existe; no reanudar ni sobrescribir')
    key = os.environ.get('ANTHROPIC_API_KEY')
    if not key:
        raise ValueError('Credencial ausente en entorno; no se carga .env automáticamente')
    source = package/'snapshots/scripts'
    budget = module(source/'ci/runtime_budget.py', 'frozen_budget')
    transport = module(source/'evaluations/foundry_native_transport.py', 'frozen_transport')
    with budget.Proxy('claude', key, amount, model=config['model'], max_requests=56, max_output_tokens=config['output_cap']) as proxy:
        result = execute(package, args.output, proxy, args.cli, transport,report_word_limit=config.get('report_word_limit',700))
    print(json.dumps(result))


if __name__ == '__main__':
    main()
