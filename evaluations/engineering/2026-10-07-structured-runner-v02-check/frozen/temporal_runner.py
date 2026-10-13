"""Runner temporal v0.2.0: salida estructurada nativa y validación local independiente."""
import argparse
from datetime import datetime,timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tempfile
import time
from typing import Literal
from pydantic import BaseModel,ConfigDict,Field,ValidationError,field_validator,model_validator

RUNNER_VERSION='0.2.0'
SCHEMA_VERSION='0.1.0'
ROOT=Path(__file__).resolve().parents[2]
SCHEMA_PATH=ROOT/'schemas/temporal-audit-0.1.0.schema.json'
SYSTEM='Responde en español. Realiza la auditoría con los datos provistos y entrega el objeto mediante el mecanismo de salida estructurada. No entrenes, ejecutes comandos, accedas a archivos o actúes externamente. No tienes autoridad para aprobar gates.'

class TemporalRow(BaseModel):
    model_config=ConfigDict(strict=True,extra='forbid')
    id: str=Field(min_length=1)
    outcome_state_at_extraction: Literal['observed_positive','observed_negative','pending','unknown']
    label_availability_at_training: Literal['available','unavailable','indeterminate']
    train_eligibility: Literal['eligible','exclude','indeterminate']
    reason: str=Field(min_length=1)

    @field_validator('id','reason')
    @classmethod
    def nonblank(cls,value):
        if not value.strip():raise ValueError('Texto vacío')
        try:value.encode('utf-8')
        except UnicodeEncodeError as exc:raise ValueError('Unicode inválido') from exc
        return value

class TemporalAudit(BaseModel):
    model_config=ConfigDict(strict=True,extra='forbid')
    rows: list[TemporalRow]=Field(min_length=1)
    open_questions: list[str]
    # No forzar NEEDS_REVIEW: el checker de contenido debe detectar otra decisión.
    gate_decision: Literal['NEEDS_REVIEW','PASS','BLOCKED']

    @field_validator('open_questions')
    @classmethod
    def questions_nonblank(cls,values):
        if any(not q.strip() for q in values):raise ValueError('Pregunta vacía')
        try:
            for question in values:question.encode('utf-8')
        except UnicodeEncodeError as exc:raise ValueError('Unicode inválido') from exc
        return values

    @model_validator(mode='after')
    def unique_ids(self):
        if len({row.id for row in self.rows})!=len(self.rows):raise ValueError('IDs duplicados')
        return self

def schema_document():
    schema=TemporalAudit.model_json_schema()
    # Claude acepta draft-07; convertir los $defs/$ref de Pydantic a definitions.
    schema['definitions']=schema.pop('$defs')
    schema['properties']['rows']['items']['$ref']='#/definitions/TemporalRow'
    schema['$schema']='http://json-schema.org/draft-07/schema#'
    schema['$comment']='ACOS temporal-audit '+SCHEMA_VERSION+'; estructura, no expected ni aprobación humana.'
    return schema

def now():return datetime.now(timezone.utc).isoformat()
def digest(data):return hashlib.sha256(data).hexdigest()
def write_json(path,data):path.write_text(json.dumps(data,ensure_ascii=True,indent=2,allow_nan=False)+'\n',encoding='utf-8')

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Clave duplicada: '+key)
        result[key]=value
    return result

def reject_constant(value):raise ValueError('Número no finito: '+value)
def finite_float(value):
    number=float(value)
    if not math.isfinite(number):raise ValueError('Número fuera de rango finito')
    return number

def decode(raw):return json.loads(raw,object_pairs_hook=unique_object,parse_constant=reject_constant,parse_float=finite_float)

def run_one(payload_file,output_dir,cli_argv,model):
    payload=Path(payload_file).read_bytes();schema_bytes=SCHEMA_PATH.read_bytes()
    schema=decode(schema_bytes)
    if schema!=schema_document():raise ValueError('Schema y validador local difieren; revisar versiones antes de ejecutar.')
    target=Path(output_dir);target.mkdir(parents=True,exist_ok=False)
    (target/'payload.txt').write_bytes(payload);(target/'schema.json').write_bytes(schema_bytes)
    findings=[]
    try:
        version=subprocess.run([*cli_argv,'--version'],capture_output=True,text=True,timeout=30,check=True).stdout.strip()
    except (OSError,subprocess.SubprocessError):
        version='UNKNOWN';findings.append({'code':'cli-version','message':'No se pudo comprobar versión CLI.'})
    argv=[*cli_argv,'-p','--safe-mode','--no-chrome','--no-session-persistence','--tools','',
          '--strict-mcp-config','--mcp-config','{"mcpServers":{}}','--output-format','json',
          '--json-schema',schema_bytes.decode(),'--model',model,'--effort','medium','--system-prompt',SYSTEM]
    started=now();start=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='acos-structured-call-') as work:
        request={'argv':argv,'cwd':work,'stdin_sha256':digest(payload),'schema_sha256':digest(schema_bytes),
                 'system_prompt':SYSTEM,'cli_version':version,'runner_version':RUNNER_VERSION,'schema_version':SCHEMA_VERSION}
        write_json(target/'request.json',request)
        try:
            process=subprocess.run(argv,input=payload,cwd=work,capture_output=True,timeout=180,env=os.environ.copy())
            stdout,stderr,exit_code=process.stdout,process.stderr,process.returncode
        except subprocess.TimeoutExpired as exc:
            stdout,stderr,exit_code=exc.stdout or b'',exc.stderr or b'',124
        except OSError as exc:
            stdout,stderr,exit_code=b'',str(exc).encode(),126
        (target/'stdout.txt').write_bytes(stdout);(target/'raw.json').write_bytes(stdout);(target/'stderr.txt').write_bytes(stderr)
        try:raw=decode(stdout)
        except (ValueError,UnicodeDecodeError):
            raw=None;findings.append({'code':'raw-invalid','message':'Envelope JSON ausente o inválido; stdout preservado.'})
        runtime_success=exit_code==0 and isinstance(raw,dict) and raw.get('type')=='result' and raw.get('subtype')=='success' and raw.get('is_error') is False
        if not runtime_success:findings.append({'code':'runtime-failed','message':'Runtime no completó con éxito.'})
        structured_present=isinstance(raw,dict) and 'structured_output' in raw
        schema_conformant=False
        if isinstance(raw,dict) and isinstance(raw.get('result'),str):
            try:result_bytes=raw['result'].encode('utf-8')
            except UnicodeEncodeError:
                write_json(target/'result-escaped.json',raw['result'])
                findings.append({'code':'result-unicode-invalid','message':'Texto opcional con Unicode inválido; conservado como JSON escapado.'})
            else:(target/'result.txt').write_bytes(result_bytes)
        if structured_present:
            structured=raw['structured_output']
            write_json(target/'structured-output.json',structured)
            try:
                TemporalAudit.model_validate(structured,strict=True)
                schema_conformant=True
            except ValidationError as exc:
                findings.append({'code':'structured-invalid','message':'Objeto estructurado no cumple validación local.',
                                 'errors':exc.errors(include_url=False,include_context=False,include_input=False)})
        else:findings.append({'code':'structured-missing','message':'Falta structured_output; result no lo sustituye.'})
        usage_reported=raw.get('modelUsage') if isinstance(raw,dict) else None
        usage=usage_reported if isinstance(usage_reported,dict) else {}
        model_matches=set(usage)=={model}
        if not model_matches:findings.append({'code':'model-unverified','message':'Modelo resuelto distinto o desconocido.'})
        metadata={'runner_version':RUNNER_VERSION,'schema_version':SCHEMA_VERSION,'started_at':started,'finished_at':now(),
            'wall_seconds':round(time.monotonic()-start,3),'provider_duration_ms':raw.get('duration_ms') if isinstance(raw,dict) else None,
            'exit_code':exit_code,'runtime_success':runtime_success,'structured_present':structured_present,'schema_conformant':schema_conformant,
            'model_matches':model_matches,'content_validation':'NOT_RUN','findings':findings,
            'session_id':raw.get('session_id') if isinstance(raw,dict) else None,
            'num_turns':raw.get('num_turns') if isinstance(raw,dict) else None,
            'model_usage':usage,'model_usage_reported':usage_reported,'cost_usd_reported':raw.get('total_cost_usd') if isinstance(raw,dict) else None,
            'cli_version':version,'platform':platform.platform(),'python_version':platform.python_version(),
            'payload_sha256':digest(payload),'schema_sha256':digest(schema_bytes),'request_sha256':digest((target/'request.json').read_bytes()),
            'runner_sha256':digest(Path(__file__).read_bytes()),
            'effective_configuration':{'resolved_models':list(usage),'effort':'unknown','tools':'unknown','safe_mode':'unknown','mcp':'unknown','session_persistence':'unknown'},
            'artifact_sha256':{p.name:digest(p.read_bytes()) for p in sorted(target.iterdir()) if p.is_file()}}
        write_json(target/'metadata.json',metadata)
    return metadata

def main(argv=None):
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--payload-file',type=Path,required=True,help='Payload confirmado, sin expected')
    parser.add_argument('--output-dir',type=Path,required=True,help='Carpeta nueva para conservar el intento')
    parser.add_argument('--model',default='claude-sonnet-5-5',help='Modelo solicitado explícitamente')
    args=parser.parse_args(argv)
    try:
        cli=shutil.which('claude')
        if not cli:raise ValueError('Claude CLI no disponible')
        result=run_one(args.payload_file,args.output_dir,[cli],args.model)
        print(json.dumps({key:result[key] for key in ('runner_version','runtime_success','schema_conformant','model_matches','content_validation','cost_usd_reported','findings')},ensure_ascii=True,indent=2))
        return 0 if result['runtime_success'] and result['schema_conformant'] and result['model_matches'] and result['cli_version']!='UNKNOWN' else 4
    except (ValueError,OSError) as exc:
        print('Entrada/operación inválida: '+str(exc));return 2

if __name__=='__main__':raise SystemExit(main())
