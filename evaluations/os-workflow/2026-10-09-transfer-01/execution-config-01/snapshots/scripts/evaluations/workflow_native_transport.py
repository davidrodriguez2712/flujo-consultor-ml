"""Transporte nativo de la evaluación; importar no hace llamadas de modelos.

El coordinador debe comprobar autorización/hash antes de crear el proxy y
parar tras cualquier fallo. Cada invoke habilita un único request adicional.
"""
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import tempfile

MODEL='claude-haiku-5-5'
SYSTEM='Responde en español y cumple el contrato JSON incluido en el expediente. Revisa únicamente el contenido proporcionado. No uses herramientas ni apruebes gates.'

TRANSFER_SYSTEM='Responde en español y cumple el contrato de salida específico incluido en el expediente. Revisa únicamente el contenido proporcionado. No uses herramientas ni apruebes gates.'

def require_approval(approval, manifest_sha):
    amount=approval.get('total_budget_usd')
    if (approval.get('status')!='APPROVED' or
        approval.get('execution_manifest_sha256')!=manifest_sha or
        isinstance(amount,bool) or not isinstance(amount,(int,float)) or not 0<amount<=0.20):
        raise ValueError('Falta autorización de gasto ligada a esta configuración (hasta US$0.20).')
    return amount


def invoke(payload, output, proxy, cli, *, system_prompt=SYSTEM):
    target=Path(output)
    target.mkdir(parents=True,exist_ok=False)
    (target/'payload.txt').write_text(payload,encoding='utf-8')
    start=len(proxy.budget.entries)
    if start>=13:raise ValueError('Límite de 13 solicitudes para esta ronda')
    proxy.budget.max_requests=start+1
    argv=[str(cli),'-p','--bare','--safe-mode','--no-chrome','--no-session-persistence',
          '--disable-slash-commands','--tools','', '--strict-mcp-config','--mcp-config','{"mcpServers":{}}',
          '--setting-sources','', '--effort','low','--model',MODEL,
          '--system-prompt',system_prompt,'--output-format','json']
    env={k:v for k,v in os.environ.items() if k in {'PATH','HOME','TMPDIR','LANG','LC_ALL','SYSTEMROOT'}}
    env.update(ANTHROPIC_API_KEY='local-proxy-placeholder',ANTHROPIC_BASE_URL=proxy.url,
               CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC='1',ANTHROPIC_MAX_RETRIES='0')
    metadata={'started_at':datetime.now(timezone.utc).isoformat(),'argv':argv,
              'runtime_success':False,'usage_known':False,'request_count':0,'semantic_review':'NOT_RUN'}
    stdout=stderr='';returncode=None
    with tempfile.TemporaryDirectory(prefix='acos-workflow-native-') as cwd:
        metadata['temporary_cwd']=cwd
        try:
            result=subprocess.run(argv,input=payload,text=True,encoding='utf-8',capture_output=True,
                                  cwd=cwd,env=env,timeout=180,check=False)
            stdout,stderr,returncode=result.stdout,result.stderr,result.returncode
        except subprocess.TimeoutExpired as exc:
            stdout=exc.stdout or '';stderr=exc.stderr or ''
            if isinstance(stdout,bytes):stdout=stdout.decode('utf-8',errors='replace')
            if isinstance(stderr,bytes):stderr=stderr.decode('utf-8',errors='replace')
            metadata['transport_error']='timeout'
        except OSError:
            metadata['transport_error']='native-launch-failed'
    stdout=stdout.replace(proxy.key,'[REDACTED]');stderr=stderr.replace(proxy.key,'[REDACTED]')
    (target/'stdout.txt').write_text(stdout,encoding='utf-8')
    (target/'stderr.txt').write_text(stderr,encoding='utf-8')
    entries=proxy.budget.entries[start:]
    metadata.update(returncode=returncode,request_count=len(entries),
                    usage_known=len(entries)==1 and entries[0].get('estimated_usd') is not None)
    try:
        envelope=json.loads(stdout)
        model_usage=envelope.get('modelUsage')
        model_ok=isinstance(model_usage,dict) and set(model_usage)=={MODEL}
        text=envelope.get('result')
        if isinstance(text,str):(target/'result.txt').write_text(text,encoding='utf-8')
        metadata['runtime_success']=(returncode==0 and envelope.get('type')=='result' and
            envelope.get('subtype')=='success' and envelope.get('is_error') is False and
            model_ok and isinstance(text,str) and len(entries)==1 and metadata['usage_known'] and
            not entries[0].get('bound_exceeded') and not entries[0].get('transport_error'))
        metadata['model_usage']=model_usage
    except (ValueError,TypeError,AttributeError):
        metadata['envelope_error']='invalid-json-envelope'
    metadata['finished_at']=datetime.now(timezone.utc).isoformat()
    (target/'metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    return metadata
