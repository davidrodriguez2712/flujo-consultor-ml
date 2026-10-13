"""Ejemplo local del procedimiento; no implementa validación automática de ACOS.

Desde el checkout: PYTHONPATH=src .venv/bin/python docs/acos/validation/serialization-example.py
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import tempfile

from acos.catalog import load_catalog
from acos.compiler import compile_project
from acos.contracts import ProjectProfile
from acos.foundry import scan_foundry
from acos.resolver import confirm_plan, resolve


def run():
    root = Path(__file__).resolve().parents[3]
    destination = Path(tempfile.mkdtemp(prefix='acos-serialization-')).resolve()
    project = destination/'example'
    profile = ProjectProfile(project={'slug':'serialization-demo','name':'Reproducción demo'},data={'sources':['csv']})
    plan = confirm_plan(resolve(profile,load_catalog(),scan_foundry(None)),True)
    manifest = compile_project(plan,project,False)
    assert (project/'templates/delivery-and-handoff.md').is_file()
    assert any(entry['path']=='templates/delivery-and-handoff.md' for entry in manifest.artifacts)
    for rel in ('workflow/execution-and-qa.md','templates/delivery-and-handoff.md','templates/data-and-validation.md','playbooks/data-understanding-analysis.md','playbooks/experiments-and-models.md'):
        assert (root/rel).read_bytes()==(root/'src/acos/resources/os'/rel).read_bytes()

    # Criterios previos: mismo ID y regla; valores con tolerancia; selección exacta.
    rtol, atol = 1e-8, 1e-6
    threshold = 0.3
    memory_rows = [{'id':'001','value':0.1+0.2}]
    persisted = project/'example.csv'
    # Precisión explícita del writer de este ejemplo, no un default universal de CSV.
    with persisted.open('w',encoding='utf-8',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=['id','value'])
        writer.writeheader()
        for row in memory_rows:
            writer.writerow({'id':row['id'],'value':format(row['value'],'.16g')})
    original_hash = hashlib.sha256(persisted.read_bytes()).hexdigest()

    def read_rows(path=persisted):
        with path.open(encoding='utf-8',newline='') as stream:
            return [{'id':row['id'],'value':float(row['value'])} for row in csv.DictReader(stream)]

    def selection(rows):
        return [row['id'] for row in rows if row['value']>threshold]

    original_rows = read_rows()
    original_selection = selection(original_rows)
    omitted_boundary_selection = selection(memory_rows)
    reproduced = project/'reproduced.csv'
    with reproduced.open('w',encoding='utf-8',newline='') as stream:
        writer = csv.DictWriter(stream,fieldnames=['id','value'])
        writer.writeheader()
        for row in memory_rows:
            writer.writerow({'id':row['id'],'value':format(row['value'],'.16g')})
    faithful_rows = read_rows(reproduced)
    faithful_selection = selection(faithful_rows)
    values_close = math.isclose(memory_rows[0]['value'],original_rows[0]['value'],rel_tol=rtol,abs_tol=atol)
    assert original_rows == [{'id':'001','value':0.3}]
    assert values_close
    assert original_selection == []
    assert omitted_boundary_selection == ['001']
    assert faithful_selection == original_selection
    assert faithful_rows == original_rows
    assert hashlib.sha256(persisted.read_bytes()).hexdigest() == original_hash
    result = {
        'scenario':'explicit-serialization-boundary','result':'PASS',
        'writer':{'format':'csv','encoding':'utf-8','numeric_format':'.16g'},
        'reader':{'id':'str','value':'float'},
        'criteria':{'rtol':rtol,'atol':atol,'selection':'exact','threshold':threshold,'rule':'value > threshold'},
        'original':{'value':original_rows[0]['value'],'selection':original_selection},
        'omitted_boundary':{'value':memory_rows[0]['value'],'numeric_within_tolerance':values_close,'selection':omitted_boundary_selection,'comparison':'DISCREPANCY'},
        'faithful_reproduction':{'selection':faithful_selection,'comparison':'PASS'},
        'original_csv_unchanged':True,'api_cost_usd':0,
        'limits':'Ejemplo de threshold con writer explícito; no demuestra eficacia de skills ni reproduce el entrenamiento del piloto.'
    }
    # Conservar ambos recorridos en el destino temporal; no sobrescribir el original.
    (destination/'comparison.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    return result


if __name__=='__main__':
    print(json.dumps(run(),ensure_ascii=False,indent=2))
