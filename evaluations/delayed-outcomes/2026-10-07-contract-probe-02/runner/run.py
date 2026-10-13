"""Runner local reproducible de 24 calls; no contiene expected en payloads."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import time

SYSTEM='Responde en español. Sigue la tarea y devuelve exclusivamente el JSON pedido. No tienes autoridad para aprobar gates. No uses herramientas.'

def now():return datetime.now(timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def write_json(path,data):path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def prepare(root):
    if (root/'frozen-inputs.json').exists():raise ValueError('Ronda congelada; no sobrescribir preparación.')
    base=(root/'guidance/baseline-design-validation-0.1.0.md').read_text()
    contract=(root/'guidance/temporal-contract-0.1.0.md').read_text()
    task=(root/'task.md').read_text()
    for case in 'ABCDEF':
        folder=root/'payloads'/case;folder.mkdir(parents=True,exist_ok=True)
        payload='# Pautas actuales\n'+base+'\n# Tarea\n'+task+'\n# Caso\n'+(root/'cases'/case/'case.md').read_text()+'\n# Inputs\n'+(root/'cases'/case/'inputs.json').read_text()
        (folder/'baseline.txt').write_text(payload)
        (folder/'treatment.txt').write_text(payload+'\n# Contrato temporal adicional\n'+contract)
    plan=[]
    for repetition in (1,2):
        for case in 'ABCDEF':
            baseline_first=(case in 'ACE') if repetition==1 else (case in 'BDF')
            for branch in (('baseline','treatment') if baseline_first else ('treatment','baseline')):
                plan.append({'case':case,'branch':branch,'repetition':repetition})
    write_json(root/'plan.json',plan)
    return plan

def frozen_files(root):
    return {str(p.relative_to(root)):digest(p.read_bytes()) for p in sorted(root.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts
            and p.name not in ('frozen-inputs.json','provenance.json') and 'runs' not in p.relative_to(root).parts}

def freeze(root,version):
    if (root/'frozen-inputs.json').exists():raise ValueError('Ya está congelada.')
    write_json(root/'frozen-inputs.json',frozen_files(root))
    write_json(root/'provenance.json',{'frozen_at':now(),'precedence_evidence':'local_only',
        'user_approved_design':True,'claude_cli_version':version,'platform':platform.platform(),
        'python_version':platform.python_version(),'system_prompt':SYSTEM,
        'source':'Foundry canónico design-validation 0.1.0 snapshot; contrato local 0.1.0',
        'requested_configuration':{'model':'claude-sonnet-5-5','effort':'medium','safe_mode':True,'tools':[],'mcp_servers':{},'session_persistence':False},
        'note':'Flags registrados no acreditan por sí mismos la configuración efectiva del proveedor.'})

def verify_frozen(root):
    for rel,want in json.loads((root/'frozen-inputs.json').read_text()).items():
        if digest((root/rel).read_bytes())!=want:raise ValueError('Input congelado alterado: '+rel)

def run_one(root,case,branch,repetition,cli_argv,model,version):
    target=root/'runs'/case/branch/str(repetition)
    target.mkdir(parents=True,exist_ok=False)
    payload=(root/'payloads'/case/(branch+'.txt')).read_bytes()
    (target/'payload.txt').write_bytes(payload)
    argv=[*cli_argv,'-p','--safe-mode','--no-chrome','--no-session-persistence','--tools','',
          '--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--output-format','json',
          '--model',model,'--effort','medium','--system-prompt',SYSTEM]
    started=now();start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='acos-temporal02-call-') as work:
        request={'argv':argv,'cwd':work,'stdin_sha256':digest(payload),'system_prompt':SYSTEM,'cli_version':version}
        write_json(target/'request.json',request)
        # Heredar autenticación; no copiar ni imprimir variables privadas.
        try:
            process=subprocess.run(argv,input=payload,cwd=work,capture_output=True,timeout=180,env=os.environ.copy())
            stdout,stderr,exit_code=process.stdout,process.stderr,process.returncode
        except subprocess.TimeoutExpired as exc:
            stdout,stderr,exit_code=exc.stdout or b'',exc.stderr or b'',124
        (target/'stdout.txt').write_bytes(stdout);(target/'stderr.txt').write_bytes(stderr)
        try:raw=json.loads(stdout)
        except (ValueError,UnicodeDecodeError):raw=None
        runtime_ok=exit_code==0 and isinstance(raw,dict) and isinstance(raw.get('result'),str) and not raw.get('is_error',False)
        if isinstance(raw,dict):
            (target/'raw.json').write_bytes(stdout)
            if isinstance(raw.get('result'),str):(target/'result.txt').write_text(raw['result'])
        usage_reported=raw.get('modelUsage',{}) if isinstance(raw,dict) else {}
        usage=usage_reported if isinstance(usage_reported,dict) else {}
        runtime_ok=runtime_ok and isinstance(usage_reported,dict)
        metadata={'case':case,'branch':branch,'repetition':repetition,'started_at':started,'finished_at':now(),
            'wall_seconds':round(time.monotonic()-start,3),'provider_duration_ms':raw.get('duration_ms') if isinstance(raw,dict) else None,
            'exit_code':exit_code,'runtime_ok':runtime_ok,'session_id':raw.get('session_id') if isinstance(raw,dict) else None,
            'is_error':raw.get('is_error') if isinstance(raw,dict) else None,
            'model_usage':usage,'model_usage_reported':usage_reported,'cost_usd':raw.get('total_cost_usd') if isinstance(raw,dict) else None,
            'cli_version':version,'cwd':work,'payload_sha256':digest(payload),
            'request_sha256':digest((target/'request.json').read_bytes()),
            'effective_configuration':{'resolved_models':list(usage),'effort':'unknown','tools':'not independently exposed','safe_mode':'not independently exposed','mcp':'not independently exposed','session_persistence':'not independently exposed'}}
        write_json(target/'metadata.json',metadata)
    return metadata

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--prepare',action='store_true');parser.add_argument('--freeze',action='store_true');parser.add_argument('--run',action='store_true')
    args=parser.parse_args();root=Path(__file__).resolve().parents[1]
    cli=shutil.which('claude')
    if not cli:raise ValueError('Claude CLI no disponible')
    version=subprocess.run([cli,'--version'],capture_output=True,text=True,check=True).stdout.strip()
    if args.prepare:prepare(root)
    if args.freeze:freeze(root,version)
    if args.run:
        verify_frozen(root)
        provenance=json.loads((root/'provenance.json').read_text())
        if provenance['claude_cli_version']!=version:raise ValueError('Cambió versión CLI tras congelar.')
        for index,entry in enumerate(json.loads((root/'plan.json').read_text()),1):
            previous=root/'runs'/entry['case']/entry['branch']/str(entry['repetition'])/'metadata.json'
            if previous.exists():
                saved=json.loads(previous.read_text())
                if set(saved.get('model_usage',{}))!={'claude-sonnet-5-5'}:raise ValueError('Modelo efectivo previo distinto/desconocido; detener comparación.')
                if saved.get('cli_version')!=version:raise ValueError('Versión CLI de intento previo cambió.')
                if saved['runtime_ok']:continue
                raise ValueError('Intento fallido conservado; requiere revisión y protocolo explícito para reanudar.')
            record=run_one(root,**entry,cli_argv=[cli],model='claude-sonnet-5-5',version=version)
            print(json.dumps({'index':index,**entry,'runtime_ok':record['runtime_ok'],'wall_seconds':record['wall_seconds'],'cost_usd':record['cost_usd']},ensure_ascii=False),flush=True)
            verify_frozen(root)
            if not record['runtime_ok']:return 4
            if set(record['model_usage'])!={'claude-sonnet-5-5'}:raise ValueError('Modelo efectivo distinto/desconocido; detener comparación.')
    return 0

if __name__=='__main__':raise SystemExit(main())
