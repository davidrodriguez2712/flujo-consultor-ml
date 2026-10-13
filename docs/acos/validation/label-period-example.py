"""Ejemplo del procedimiento de QA, sin automatizar checks de entregables en ACOS.

Ejecutar desde el checkout con PYTHONPATH=src .venv/bin/python seguido de esta ruta.
"""
from datetime import date
from itertools import permutations
import json
from pathlib import Path
import tempfile

from acos.catalog import load_catalog
from acos.compiler import compile_project
from acos.contracts import ProjectProfile
from acos.foundry import scan_foundry
from acos.resolver import confirm_plan, resolve


def latest_complete(rows):
    candidates=[r for r in rows if r['method']=='baseline' and r['metric']=='retention' and r['population']=='eligible_customers' and r['complete']]
    if not candidates:
        raise ValueError('No hay períodos completos elegibles.')
    keys=[(r['method'],r['metric'],r['population'],r['cutoff']) for r in candidates]
    if len(keys)!=len(set(keys)):
        raise ValueError('Keys duplicadas: resultado ambiguo.')
    return max(candidates,key=lambda r:date.fromisoformat(r['cutoff']))


def run():
    root=Path(__file__).resolve().parents[3]
    destination=Path(tempfile.mkdtemp(prefix='acos-label-qa-')).resolve()
    project=destination/'example'
    profile=ProjectProfile(project={'slug':'label-demo','name':'QA de períodos demo'})
    plan=confirm_plan(resolve(profile,load_catalog(),scan_foundry(None)),True)
    manifest=compile_project(plan,project,False)
    assert (project/'templates/findings-and-qa.md').is_file()
    assert any(a['path']=='templates/findings-and-qa.md' for a in manifest.artifacts)
    for rel in ('templates/findings-and-qa.md','workflow/execution-and-qa.md'):
        assert (root/rel).read_bytes()==(root/'src/acos/resources/os'/rel).read_bytes()
    rows=[
        {'method':'baseline','metric':'retention','population':'eligible_customers','cutoff':'2026-06-01','complete':True,'value':0.25},
        {'method':'baseline','metric':'retention','population':'eligible_customers','cutoff':'2026-12-01','complete':False,'value':0.8},
        {'method':'challenger','metric':'retention','population':'eligible_customers','cutoff':'2026-09-01','complete':True,'value':0.9},
        {'method':'baseline','metric':'retention','population':'eligible_customers','cutoff':'2026-09-01','complete':True,'value':0.6},
    ]
    expected=latest_complete(rows)
    assert expected['cutoff']=='2026-09-01' and expected['value']==0.6
    positional=rows[0]
    assert positional['value']==0.25 # Cifra válida, identidad incorrecta para “último”.
    assert positional['cutoff']!=expected['cutoff']
    observed_latest=max((r for r in rows if r['method']=='baseline'),key=lambda r:date.fromisoformat(r['cutoff']))
    assert observed_latest['cutoff']=='2026-12-01' and not observed_latest['complete']
    for ordered in permutations(rows):
        assert latest_complete(ordered)==expected
    for invalid_rows in ([rows[1]],[*rows,dict(rows[3])]):
        try:
            latest_complete(invalid_rows)
        except ValueError:
            pass
        else:
            raise AssertionError('Debe rechazar ausencia de períodos completos o keys duplicadas.')
    original={'label':'Último período completo del baseline','cutoff':positional['cutoff'],'value':positional['value']}
    corrected={'label':'Último período completo del baseline: 2026-09-01','cutoff':expected['cutoff'],'value':expected['value']}
    (destination/'original.json').write_text(json.dumps(original,indent=2))
    (destination/'correction.json').write_text(json.dumps({'original':'original.json','corrected':corrected,'reason':'Índice posicional atribuyó junio al último período completo.'},ensure_ascii=False,indent=2))
    assert json.loads((destination/'original.json').read_text())==original
    return {
        'scenario':'labels-and-complete-periods','result':'PASS',
        'valid_number_wrong_period':{'value':positional['value'],'cutoff':positional['cutoff'],'comparison':'DISCREPANCY'},
        'latest_observed_incomplete':observed_latest['cutoff'],
        'latest_complete_baseline':corrected,
        'row_order_permutations_checked':24,
        'ambiguous_keys_rejected':True,'no_complete_period_rejected':True,
        'original_preserved':True,'api_cost_usd':0,
        'limits':'Ejemplo con regla explícita de elegibilidad; no interpreta texto libre ni prueba eficacia de skills.'
    }


if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
