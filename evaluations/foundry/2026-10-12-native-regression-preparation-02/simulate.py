"""Probe local de infraestructura: HTTPS sustituido; sin credenciales reales.

Los reportes y el ledger son sintéticos, no evidencia de eficacia de un LLM.
Este script pertenece al experimento, no al producto ni al entrypoint pagado.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import shlex
import shutil
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parent


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def sequence_for(package, output, study, transport, helper):
    events = []
    for case, condition in study.SCHEDULE:
        source = package/'public'/case
        root = output/(case+'-'+condition)/'workspace'
        rows = [source/'case.md', *sorted((source/'inputs').rglob('*'))]
        content = ('---\nskill: detect-leakage\nversion: "0.2.0"\nfecha: 2026-10-12\n'
                   'estado: infraestructura_simulada\ncondicion: treatment\ninputs:\n')
        for path in rows:
            if path.is_file():
                content += ('  - path: '+str(path.relative_to(source))+'\n    sha256: '
                            +hashlib.sha256(path.read_bytes()).hexdigest()+'\n')
        content += '---\n'
        for title in ['Resumen', 'Hallazgos', 'Evidencia', 'Preguntas abiertas', 'Recomendaciones']:
            content += '## '+title+'\nRespuesta sintética; no se evalúa contenido del caso ni eficacia.\n'
        calls = [
            ('Skill', {'skill': transport.SKILL}),
            ('Bash', {'command': shlex.join([sys.executable, str(root/'.runtime/check_inputs.py')])}),
            ('Write', {'file_path': str(root/'reports/leakage/audit.md'), 'content': content}),
        ]
        for index, (name, args) in enumerate(calls):
            events.append(helper.sse(transport.MODEL, [{'type': 'tool_use', 'id': case+str(index),
                          'name': name, 'input': args}], 'tool_use'))
        events.append(helper.sse(transport.MODEL, [{'type': 'text',
                      'text': 'Reporte sintético en reports/leakage/audit.md; semántica no evaluada.'}], 'end_turn'))
    return events


def main():
    package = ROOT/'package'
    code = package/'snapshots/scripts'
    study = module(code/'evaluations/foundry_study.py', 'simulated_frozen_study')
    config, manifest = study.verify(package)
    try:
        study.require_approval(json.loads((ROOT/'approval.json').read_text()), manifest)
    except ValueError:
        rejected = True
    else:
        raise RuntimeError('Esta preparación no debe autorizar llamadas de pago')
    helper = module(ROOT/'probe-support/test_foundry_native_transport.py', 'simulated_provider_helpers')
    cli = shutil.which('claude')
    if not cli or subprocess.run([cli, '--version'], check=True, capture_output=True, text=True).stdout.strip() != config['cli_version']:
        raise RuntimeError('CLI distinta del snapshot')
    results = []
    # El límite 0.10 es ficticio dentro del proveedor simulado, no presupuesto real.
    for name, limit in [('nominal-simulated', .10), ('remaining-budget-simulated', .00887352)]:
        output = ROOT/'runs'/name
        transport = module(code/'evaluations/foundry_native_transport.py', 'simulated_frozen_transport_'+name)
        budget = module(code/'ci/runtime_budget.py', 'simulated_frozen_budget_'+name)
        sequence = sequence_for(package, output, study, transport, helper)
        with pytest.MonkeyPatch.context() as patch:
            # Todas las conexiones HTTPS upstream de este proxy terminan en SSE fijo.
            requests = helper.fake_upstream(budget, patch, sequence)
            with budget.Proxy('claude', 'fake-simulation-placeholder', limit, model=config['model'],
                              max_requests=56, max_output_tokens=config['output_cap']) as proxy:
                result = study.execute(package, output, proxy, cli, transport,
                                       report_word_limit=config['report_word_limit'])
                results.append({'name': name, 'synthetic_budget_usd': limit,
                                'status': result['status'], 'runs': result['runs'],
                                'simulated_provider_requests': len(requests),
                                'real_provider_requests': 0, 'real_api_cost_usd': 0,
                                'rejections': proxy.rejections,
                                'synthetic_ledger_only': True})
    summary = {'execution_manifest_sha256': manifest, 'paid_approval_rejected': rejected,
               'mode': 'REAL_CLI_SIMULATED_PROVIDER_NOT_LLM_EFFICACY', 'results': results}
    (ROOT/'simulation-summary.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2)+'\n')
    assert results[0]['status'] == 'COMPLETED_PENDING_CONTENT_REVIEW', summary
    assert len(results[0]['runs']) == 3 and all(x['contract_success'] for x in results[0]['runs'])
    assert results[1]['status'] == 'STOPPED_RUNTIME_FAILURE', summary
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
