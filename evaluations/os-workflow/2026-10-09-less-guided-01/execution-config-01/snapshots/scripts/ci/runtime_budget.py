"""Proxy local del probe: reserva antes de enviar, sin retries ni logs de claves.

No es un sistema de facturación. Reserva bytes UTF-8 + margen de serialización
como cota conservadora de tokens para estos requests textuales; el informe
separa reserva, usage observado y estimación de coste. No incluye GitHub Actions.
"""
import http.client
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import threading

MODELS = {'codex': 'gpt-6-luna', 'claude': 'claude-haiku-4-5-20251001'}


class Budget:
    def __init__(self, limit, max_requests=16):
        if not 0 < limit <= 0.5: raise ValueError('presupuesto inválido')
        self.limit = limit
        self.max_requests = max_requests
        self.entries = []
        self.lock = threading.Lock()

    @property
    def committed(self):
        return sum(e['committed_usd'] for e in self.entries)

    def reserve(self, amount):
        with self.lock:
            if len(self.entries) >= self.max_requests: raise ValueError('límite de solicitudes')
            if amount <= 0 or self.committed + amount > self.limit: raise ValueError('límite de presupuesto')
            self.entries.append({'reserved_usd': amount, 'committed_usd': amount,
                                 'estimated_usd': None, 'usage': None})
            return len(self.entries) - 1

    def finish(self, identifier, cost, usage=None):
        with self.lock:
            entry = self.entries[identifier]
            entry['usage'] = usage
            if cost is not None:
                entry['estimated_usd'] = cost
                if cost > entry['reserved_usd']:
                    # Detener solicitudes posteriores si la cota no fue suficiente.
                    self.max_requests = len(self.entries)
                    entry['bound_exceeded'] = True
                    entry['committed_usd'] = cost
                else: entry['committed_usd'] = cost


def usage_cost(runtime, usage, model=None):
    if runtime == 'codex':
        if 'input_tokens' not in usage or 'output_tokens' not in usage: return None
        # Tarifa standard Luna; separar cache read/write cuando hay metadata.
        details = usage.get('input_tokens_details', {})
        reads = details.get('cached_tokens', 0)
        writes = details.get('cache_write_tokens', 0)
        fresh = max(0, usage['input_tokens'] - reads - writes)
        return (fresh * 0.1 + reads * 0.01 + writes * 0.125 + usage['output_tokens'] * 0.5) / 1_000_000
    required = {'input_tokens', 'output_tokens'}
    if not required.issubset(usage): return None
    cache = usage.get('cache_creation', {})
    one_hour = cache.get('ephemeral_1h_input_tokens', 0)
    writes = usage.get('cache_creation_input_tokens', 0)
    rates = (1, 5, 1.25, 2, 0.1)
    if model == 'claude-haiku-5-5':
        total = usage['input_tokens'] + writes + usage.get('cache_read_input_tokens', 0)
        rates = (0.1, 0.5, 0.125, 0.2, 0.01) if total <= 100_000 else (0.5, 2.5, 0.625, 1, 0.05)
    fresh, output, short, long, read = rates
    return (usage['input_tokens'] * fresh + usage['output_tokens'] * output
            + (writes - one_hour) * short + one_hour * long
            + usage.get('cache_read_input_tokens', 0) * read) / 1_000_000


def prepare(runtime, body, model=None):
    selected = model or MODELS[runtime]
    allowed = {MODELS[runtime]} | ({'claude-haiku-5-5'} if runtime == 'claude' else set())
    if selected not in allowed or body.get('model') != selected: raise ValueError('modelo no permitido')
    haiku55 = selected == 'claude-haiku-5-5'
    if haiku55 and body.get('tools'): raise ValueError('herramientas no permitidas')
    if haiku55 and (body.get('inference_geo', 'global') != 'global' or
                    body.get('service_tier', 'auto') != 'auto'):
        raise ValueError('modificador de tarifa no permitido')
    # No imágenes, audio, archivos remotos ni servicios de herramientas pagados.
    def validate(value):
        if isinstance(value, dict):
            kind = value.get('type')
            if isinstance(kind, str) and kind in {'input_image','image','input_audio','input_file','document','audio'}:
                raise ValueError('solo texto')
            for child in value.values(): validate(child)
        elif isinstance(value, list):
            for child in value: validate(child)
    validate(body)
    if runtime == 'codex':
        def local_tool(tool):
            kind = tool.get('type')
            if kind == 'namespace': return all(local_tool(t) for t in tool.get('tools', []))
            return kind in {'function', 'custom', 'local_shell'}
        if not all(local_tool(t) for t in body.get('tools', [])):
            raise ValueError('herramienta remota no permitida')
        if body.get('previous_response_id'): raise ValueError('contexto remoto no permitido')
        body['max_output_tokens'] = min(body.get('max_output_tokens', 1024), 1024)
        body['service_tier'] = 'default'
        body['store'] = False
        in_rate, out_rate, output = 0.125, 0.5, body['max_output_tokens']
    else:
        cap = 2048 if haiku55 else 1024
        body['max_tokens'] = min(body.get('max_tokens', cap), cap)
        body.pop('thinking', None)
        if haiku55:
            body['thinking'] = {'type': 'adaptive'}
            body.setdefault('output_config', {})['effort'] = 'low'
            for field in ('temperature', 'top_p', 'top_k'): body.pop(field, None)
        management = body.get('context_management')
        if isinstance(management, dict):
            management['edits'] = [e for e in management.get('edits', [])
                                   if e.get('type') != 'clear_thinking_20251015']
            if not management['edits']: body.pop('context_management', None)
        def short_cache(value):
            if isinstance(value, dict):
                if isinstance(value.get('cache_control'), dict): value['cache_control']['ttl'] = '5m'
                for child in value.values(): short_cache(child)
            elif isinstance(value, list):
                for child in value: short_cache(child)
        short_cache(body)
        in_rate, out_rate, output = 1.25, 5, body['max_tokens']
        # Reservar incluso el tier largo y cache write antes de conocer usage.
        if haiku55: in_rate, out_rate = 0.625, 2.5
    size = len(json.dumps(body, ensure_ascii=False).encode('utf-8'))
    if size > 180_000: raise ValueError('contexto demasiado grande')
    return body, ((size + 16_384) * in_rate + output * out_rate) / 1_000_000


class Proxy:
    def __init__(self, runtime, key, limit, model=None, max_requests=16):
        self.runtime, self.key = runtime, key
        self.model = model or MODELS[runtime]
        self.budget = Budget(limit, max_requests)
        self.rejections = []
        owner = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = 'HTTP/1.1'

            def log_message(self, *args): pass

            def fail(self, status, message):
                kind = {400:'invalid_request_error',401:'authentication_error',403:'permission_error',
                        429:'rate_limit_error'}.get(status, 'api_error')
                content = json.dumps({'type':'error','error': {'type': kind, 'message': message}}).encode()
                self.send_response(status)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)

            def do_GET(self): self.fail(403, 'endpoint no permitido')

            def do_POST(self):
                wanted = '/v1/responses' if runtime == 'codex' else '/v1/messages'
                if self.path.split('?')[0] != wanted:
                    self.fail(403, 'endpoint no permitido'); return
                length = int(self.headers.get('Content-Length', 0))
                if not 0 < length <= 180_000:
                    self.fail(413, 'contexto demasiado grande'); return
                body, quote = None, None
                try:
                    body = json.loads(self.rfile.read(length))
                    body, quote = prepare(runtime, body, owner.model)
                    identifier = owner.budget.reserve(quote)
                except (ValueError, TypeError) as exc:
                    owner.rejections.append({'reason':str(exc), 'request_bytes':length, 'quote_usd':quote,
                        'tool_types':[t.get('type') for t in body.get('tools', [])] if isinstance(body, dict) else []})
                    self.fail(403, 'request bloqueado antes de enviarlo'); return
                payload = json.dumps(body, ensure_ascii=False).encode('utf-8')
                host = 'api.openai.com' if runtime == 'codex' else 'api.anthropic.com'
                headers = {'Content-Type': 'application/json', 'Accept': 'text/event-stream'}
                if runtime == 'codex': headers['Authorization'] = 'Bearer ' + owner.key
                else:
                    headers['x-api-key'] = owner.key
                    headers['anthropic-version'] = '2023-06-01'
                    # Mantener el protocolo compatible; no copiar auth/headers arbitrarios.
                    if self.headers.get('anthropic-beta'):
                        headers['anthropic-beta'] = self.headers['anthropic-beta']
                connection = http.client.HTTPSConnection(host, timeout=60)
                usage, final_usage, settled = {}, False, False
                try:
                    connection.request('POST', wanted, body=payload, headers=headers)
                    response = connection.getresponse()
                    owner.budget.entries[identifier]['http_status'] = response.status
                    if response.status != 200:
                        data = response.read()
                        try:
                            error = json.loads(data).get('error', {})
                            message = str(error.get('message','proveedor rechazó la solicitud')).replace(owner.key,'[REDACTED]')[:1600]
                            owner.budget.entries[identifier]['provider_error'] = {'type':error.get('type'), 'message':message}
                        except (ValueError, AttributeError): message = 'proveedor rechazó la solicitud'
                        owner.budget.max_requests = len(owner.budget.entries)
                        self.fail(response.status, message); return
                    self.send_response(200)
                    self.send_header('Content-Type', response.getheader('Content-Type', 'text/event-stream'))
                    self.send_header('Connection', 'close')
                    self.end_headers()
                    self.close_connection = True
                    while line := response.readline():
                        if line.startswith(b'data: '):
                            try:
                                event = json.loads(line[6:])
                                if runtime == 'codex' and event.get('type') == 'response.completed':
                                    usage = event['response'].get('usage') or {}; final_usage = True
                                    owner.budget.entries[identifier]['output_types'] = [
                                        {'type':x.get('type'), 'name':x.get('name')}
                                        for x in event['response'].get('output', [])]
                                if runtime == 'claude':
                                    if event.get('type') == 'message_start':
                                        usage.update(event['message'].get('usage', {}))
                                    elif event.get('type') == 'message_delta': usage.update(event.get('usage', {}))
                                    elif event.get('type') == 'message_stop': final_usage = True
                            except (ValueError, KeyError): pass
                        # Liquidar antes de entregar el evento terminal: el CLI puede
                        # iniciar el siguiente request inmediatamente al recibirlo.
                        if final_usage and not settled:
                            owner.budget.finish(identifier, usage_cost(runtime, usage, owner.model), usage)
                            settled = True
                        self.wfile.write(line); self.wfile.flush()
                except (OSError, http.client.HTTPException):
                    owner.budget.entries[identifier]['transport_error'] = True
                finally:
                    if not settled:
                        owner.budget.finish(identifier, usage_cost(runtime, usage, owner.model) if final_usage else None,
                                            usage if final_usage else None)
                    connection.close()

        self.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        self.server.daemon_threads = True
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)

    def __enter__(self):
        self.thread.start()
        return self

    @property
    def url(self): return 'http://127.0.0.1:' + str(self.server.server_port)

    def __exit__(self, *args):
        self.server.shutdown(); self.server.server_close(); self.thread.join(timeout=5)
