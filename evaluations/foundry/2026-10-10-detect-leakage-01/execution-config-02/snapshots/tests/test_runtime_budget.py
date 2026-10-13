"""El presupuesto del probe se verifica sin proveedores ni credenciales."""
import importlib.util
from pathlib import Path
import pytest


def module():
    path = Path(__file__).parents[1] / 'scripts/ci/runtime_budget.py'
    spec = importlib.util.spec_from_file_location('runtime_budget', path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def test_reservation_blocks_before_forwarding():
    ledger = module().Budget(0.10, 3)
    ledger.reserve(0.08)
    with pytest.raises(ValueError, match='presupuesto'):
        ledger.reserve(0.03)
    assert len(ledger.entries) == 1


def test_unknown_usage_keeps_full_reservation():
    ledger = module().Budget(0.10, 3)
    identifier = ledger.reserve(0.08)
    ledger.finish(identifier, None)
    assert ledger.committed == pytest.approx(0.08)


def test_settlement_releases_only_measured_usage():
    ledger = module().Budget(0.10, 3)
    identifier = ledger.reserve(0.08)
    ledger.finish(identifier, 0.02)
    ledger.reserve(0.07)
    assert ledger.committed == pytest.approx(0.09)


def test_request_count_independent_of_cost():
    ledger = module().Budget(0.5, 1)
    ledger.reserve(0.001)
    with pytest.raises(ValueError, match='solicitudes'):
        ledger.reserve(0.001)


def test_only_selected_text_model_and_local_tools():
    m = module()
    with pytest.raises(ValueError):
        m.prepare('codex', {'model': 'expensive', 'input': []})
    with pytest.raises(ValueError):
        m.prepare('codex', {'model': m.MODELS['codex'], 'tools': [{'type': 'web_search'}]})
    with pytest.raises(ValueError):
        m.prepare('codex', {'model': m.MODELS['codex'], 'input': [{'type': 'input_image'}]})
    body, quote = m.prepare('codex', {'model': m.MODELS['codex'], 'input': 'hola', 'max_output_tokens': 999999})
    assert body['max_output_tokens'] == 1024
    assert quote > 0


def test_codex_function_namespace_is_local_but_remote_tool_is_blocked():
    m = module()
    m.prepare('codex', {'model':m.MODELS['codex'], 'tools':[
        {'type':'namespace','name':'functions','tools':[{'type':'function','name':'exec_command'}]}]})
    with pytest.raises(ValueError):
        m.prepare('codex', {'model':m.MODELS['codex'], 'tools':[
            {'type':'namespace','name':'remote','tools':[{'type':'web_search'}]}]})


def test_json_schema_type_can_be_an_object():
    m = module()
    m.prepare('codex', {'model':m.MODELS['codex'], 'tools':[
        {'type':'function','parameters':{'properties':{'type':{'type':'string'}}}}]})


def test_disabling_thinking_removes_dependent_context_edit():
    m = module()
    body, quote = m.prepare('claude', {'model':m.MODELS['claude'],
        'thinking':{'type':'enabled','budget_tokens':4096},
        'context_management':{'edits':[{'type':'clear_thinking_20251015'}]},
        'max_tokens':8192})
    assert 'thinking' not in body
    assert 'context_management' not in body


def test_claude_uses_short_cache_to_reduce_cost():
    m = module()
    body, _ = m.prepare('claude', {'model':m.MODELS['claude'],
        'system':[{'type':'text','text':'hola','cache_control':{'type':'ephemeral','ttl':'1h'}}]})
    assert body['system'][0]['cache_control']['ttl'] == '5m'


def test_price_estimate_includes_anthropic_cache_writes():
    m = module()
    assert m.usage_cost('claude', {'input_tokens': 100, 'output_tokens': 20,
                                 'cache_creation_input_tokens': 100,
                                 'cache_read_input_tokens': 100}) == pytest.approx(0.000335)


def test_bound_exceeded_stops_future_requests():
    ledger = module().Budget(0.5)
    identifier = ledger.reserve(0.01)
    ledger.finish(identifier, 0.02)
    with pytest.raises(ValueError): ledger.reserve(0.01)


def test_blocked_http_request_never_contacts_provider(monkeypatch):
    m = module()
    def forbidden(*args, **kwargs): raise AssertionError('No debe abrir conexión con proveedor')
    monkeypatch.setattr(m.http.client, 'HTTPSConnection', forbidden)
    with m.Proxy('codex', 'fake-not-a-secret', 0.00001) as proxy:
        connection = m.http.client.HTTPConnection('127.0.0.1', proxy.server.server_port)
        import json
        connection.request('POST', '/v1/responses', json.dumps({'model':m.MODELS['codex'], 'input':'hola'}),
                           {'Content-Type':'application/json'})
        response = connection.getresponse()
        assert response.status == 403
        response.read(); connection.close()
        assert not proxy.budget.entries


def test_usage_is_settled_before_terminal_event_reaches_client(monkeypatch):
    import json
    import threading
    m = module()
    release = threading.Event()
    class Response:
        status = 200
        def __init__(self): self.sent = False
        def getheader(self, *args): return 'text/event-stream'
        def readline(self):
            if not self.sent:
                self.sent = True
                return ('data: ' + json.dumps({'type':'response.completed', 'response':{
                    'usage':{'input_tokens':1,'output_tokens':1},'output':[]}}) + '\n').encode()
            release.wait(timeout=5)
            return b''
    class Connection:
        def __init__(self, *args, **kwargs): pass
        def request(self, *args, **kwargs): pass
        def getresponse(self): return Response()
        def close(self): pass
    monkeypatch.setattr(m.http.client, 'HTTPSConnection', Connection)
    with m.Proxy('codex', 'fake-key', 0.10) as proxy:
        client = m.http.client.HTTPConnection('127.0.0.1', proxy.server.server_port)
        client.request('POST', '/v1/responses', json.dumps({'model':m.MODELS['codex'],'input':'hola'}))
        response = client.getresponse()
        response.readline()
        # La conexión upstream aún no cerró: la reserva ya debe estar liquidada.
        assert proxy.budget.committed == pytest.approx(0.0000006)
        assert proxy.budget.reserve(0.09) == 1
        release.set(); response.read(); client.close()


def test_haiku55_price_uses_all_input_classes_for_context_tier():
    # Rompe si se ignora cache al elegir el tier o se aplica tarifa 4.5.
    m = module()
    usage = {'input_tokens':100, 'output_tokens':20,
             'cache_creation_input_tokens':100, 'cache_read_input_tokens':100}
    assert m.usage_cost('claude', usage, model='claude-haiku-5-5') == pytest.approx(0.0000335)
    usage = {'input_tokens':1, 'output_tokens':20, 'cache_creation_input_tokens':100000,
             'cache_creation':{'ephemeral_1h_input_tokens':100000}}
    assert m.usage_cost('claude', usage, model='claude-haiku-5-5') == pytest.approx(0.1000505)


def test_haiku55_preparation_caps_output_and_removes_incompatible_sampling():
    # Rompe si se corta a 1024, conserva thinking legacy o usa reserva de tier corto.
    m = module()
    body, quote = m.prepare('claude', {'model':'claude-haiku-5-5', 'messages':[{'role':'user','content':'hola'}],
        'max_tokens':9999, 'thinking':{'type':'enabled','budget_tokens':4000},
        'temperature':0, 'top_p':1, 'top_k':10}, model='claude-haiku-5-5')
    assert body['max_tokens'] == 2048
    assert body['thinking'] == {'type':'adaptive'}
    assert body['output_config']['effort'] == 'low'
    assert not {'temperature','top_p','top_k'} & body.keys()
    assert quote > 0.010  # Reserva con cache write largo y output largo, no tier corto.


def test_haiku55_preparation_blocks_tools_and_model_substitution():
    m = module()
    with pytest.raises(ValueError, match='herramientas'):
        m.prepare('claude', {'model':'claude-haiku-5-5','tools':[{'name':'shell'}]}, model='claude-haiku-5-5')
    with pytest.raises(ValueError, match='modelo'):
        m.prepare('claude', {'model':m.MODELS['claude']}, model='claude-haiku-5-5')
    with pytest.raises(ValueError, match='modelo'):
        m.prepare('claude', {'model':'arbitrary'}, model='arbitrary')


def test_haiku55_proxy_enforces_single_shared_request_limit_before_provider(monkeypatch):
    # Rompe si el proxy no transmite el modelo seleccionado al filtro o ignora count.
    import json
    m = module()
    def forbidden(*args, **kwargs): raise AssertionError('Proveedor prohibido en este test')
    monkeypatch.setattr(m.http.client, 'HTTPSConnection', forbidden)
    with m.Proxy('claude', 'fake-key', 0.20, model='claude-haiku-5-5', max_requests=1) as proxy:
        proxy.budget.reserve(0.001)
        client = m.http.client.HTTPConnection('127.0.0.1', proxy.server.server_port)
        client.request('POST', '/v1/messages', json.dumps({'model':'claude-haiku-5-5','messages':[]}))
        response = client.getresponse()
        assert response.status == 403
        response.read(); client.close()
        assert len(proxy.budget.entries) == 1
        assert proxy.rejections[0]['reason'] == 'límite de solicitudes'


def test_haiku55_rejects_pricing_overrides_before_reservation():
    m=module()
    for override in ({'inference_geo':'us'},{'service_tier':'priority'}):
        with pytest.raises(ValueError,match='tarifa'):
            m.prepare('claude', {'model':'claude-haiku-5-5',**override},model='claude-haiku-5-5')


def test_haiku55_explicit_output_cap_reserves_larger_request():
    # Rompe si el cap solicitado se ignora, no cambia reserva o admite cap inseguro.
    m=module()
    body={'model':'claude-haiku-5-5','messages':[{'role':'user','content':'hola'}],'max_tokens':99999}
    small,small_quote=m.prepare('claude',dict(body),model='claude-haiku-5-5')
    large,large_quote=m.prepare('claude',dict(body),model='claude-haiku-5-5',max_output_tokens=8192)
    assert small['max_tokens']==2048
    assert large['max_tokens']==8192
    assert large_quote-small_quote==pytest.approx(0.01536)
    for cap in (0,8193,True,2.5):
        with pytest.raises(ValueError):m.prepare('claude',dict(body),model='claude-haiku-5-5',max_output_tokens=cap)


def test_claude_proxy_records_upstream_stop_reason(monkeypatch):
    # Rompe si el stop del proveedor se pierde y el 403 local se confunde con él.
    import json
    m=module()
    events=[{'type':'message_start','message':{'usage':{'input_tokens':1,'output_tokens':0}}},
        {'type':'message_delta','delta':{'stop_reason':'max_tokens'},'usage':{'output_tokens':8192}},
        {'type':'message_stop'}]
    class Response:
        status=200
        def getheader(self,*args):return 'text/event-stream'
        def readline(self):return ('data: '+json.dumps(events.pop(0))+'\n').encode() if events else b''
    class Connection:
        def __init__(self,*args,**kwargs):pass
        def request(self,method,path,body,headers):
            assert json.loads(body)['max_tokens']==8192
        def getresponse(self):return Response()
        def close(self):pass
    monkeypatch.setattr(m.http.client,'HTTPSConnection',Connection)
    with m.Proxy('claude','fake-key',0.20,model='claude-haiku-5-5',max_output_tokens=8192) as proxy:
        client=m.http.client.HTTPConnection('127.0.0.1',proxy.server.server_port)
        client.request('POST','/v1/messages',json.dumps({'model':'claude-haiku-5-5','max_tokens':99999}))
        response=client.getresponse();response.read();client.close()
        assert proxy.budget.entries[0]['provider_stop_reason']=='max_tokens'
        assert proxy.budget.entries[0]['estimated_usd']==pytest.approx(0.0040961)


@pytest.mark.parametrize('name', ['Read','Write','Bash','Skill'])
def test_haiku_local_tools_require_explicit_opt_in(name):
    m=module();tool={'name':name,'input_schema':{'type':'object','properties':{}}}
    body={'model':'claude-haiku-5-5','tools':[tool]}
    with pytest.raises(ValueError):m.prepare('claude',dict(body),model='claude-haiku-5-5')
    result,_=m.prepare('claude',dict(body),model='claude-haiku-5-5',allow_local_tools=True)
    assert result['tools']==[tool]


@pytest.mark.parametrize('tool', [
    {'name':'WebFetch','input_schema':{'type':'object'}},
    {'name':'Agent','input_schema':{'type':'object'}},
    {'name':'mcp__secret','input_schema':{'type':'object'}},
    {'name':'Read','type':'web_search_20250305','input_schema':{'type':'object'}},
    {'name':'Read','input_schema':{'type':'string'}},
    {'name':'Read','input_schema':{'type':'object','$ref':'https://example.com/schema'}},
])
def test_opt_in_rejects_remote_agents_and_invalid_tool_schema(tool):
    m=module()
    with pytest.raises(ValueError):
        m.prepare('claude',{'model':'claude-haiku-5-5','tools':[tool]},
                  model='claude-haiku-5-5',allow_local_tools=True)
