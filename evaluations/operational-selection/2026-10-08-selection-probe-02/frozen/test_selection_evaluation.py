"""Salida estructurada y oracle de selección; pruebas locales sin servicio."""
import importlib.util
import json
from pathlib import Path
import sys
import pytest
ROOT=Path(__file__).resolve().parents[1]
def module(name):
 path=ROOT/'scripts/evaluations'/(name+'.py')
 assert path.exists(), 'Falta utilidad de selección aprobada: '+name
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m

def response():
 return {'output_type':'risk_ranking','selection_status':'determined','eligible_count':2,'capacity_k':1,'effective_k':1,'selected_ids':['A'],'risk_ranking_ids':['A','B'],'total_cost':None,'expected_net_value':None,'feasibility':'feasible','optimality':'not_assessed','causal_identification':{'status':'not_requested','estimand':None,'reason':'La tarea es descriptiva.'},'metrics':{'population_id':'eligible','precision':1.0,'recall':1.0,'lift':2.0,'precision_status':'identified','recall_status':'identified','lift_status':'identified','reason':'Labels completos.'},'reason':'Score máximo y capacidad respetada.','open_questions':[],'gate_decision':'NEEDS_REVIEW'}

def invoke(tmp_path,obj,structured=True,code=0):
 m=module('selection_runner');inp=tmp_path/'input';inp.write_text('Inputs, sin expected.')
 raw={'type':'result','subtype':'success','is_error':False,'result':json.dumps(obj),'modelUsage':{'stub':{}},'total_cost_usd':0}
 if structured:raw['structured_output']=obj
 cli=tmp_path/'cli.py';cli.write_text('import json,sys\nif "--version" in sys.argv: print("stub 1")\nelse:\n sys.stdin.read()\n print('+repr(json.dumps(raw))+')\n sys.exit('+str(code)+')\n')
 dest=tmp_path/'run';return m.run_one(inp,dest,[sys.executable,str(cli)],'stub'),dest

def test_native_response_and_schema(tmp_path):
 meta,d=invoke(tmp_path,response());assert meta['schema_conformant'] and meta['runtime_success'];assert meta['content_validation']=='NOT_RUN'
 m=module('selection_runner');assert json.loads(m.SCHEMA_PATH.read_text())==m.schema_document()
 assert m.schema_document()['$schema']=='http://json-schema.org/draft-07/schema#'

@pytest.mark.parametrize('defect',['duplicate','negative_capacity','blank','unicode','extra'])
def test_bad_structure_is_archived(tmp_path,defect):
 o=response()
 if defect=='duplicate':o['selected_ids']=['A','A']
 if defect=='negative_capacity':o['capacity_k']=-1
 if defect=='blank':o['reason']=' '
 if defect=='unicode':o['reason']='\ud800'
 if defect=='extra':o['expected']='A'
 meta,d=invoke(tmp_path,o);assert not meta['schema_conformant'];assert (d/'metadata.json').exists();assert json.loads((d/'structured-output.json').read_text())==o

def test_no_result_fallback(tmp_path):
 meta,d=invoke(tmp_path,response(),False);assert meta['runtime_success'] and not meta['schema_conformant'];assert not (d/'structured-output.json').exists()

def test_schema_does_not_force_correct_selection_or_gate(tmp_path):
 o=response();o['selected_ids']=['wrong'];o['gate_decision']='PASS';meta,d=invoke(tmp_path,o)
 assert meta['schema_conformant'];c=module('selection_checker').evaluate(o,response());assert not c['members_match'] and not c['gate_matches']

def test_budget_oracle_defeats_greedy():
 c=module('selection_checker');rows=[{'id':'A','cost':6,'net_value':13},{'id':'B','cost':5,'net_value':10},{'id':'C','cost':5,'net_value':10}]
 result=c.enumerate_optimum(rows,2,10)
 assert result['selected_ids']==['B','C'] and result['expected_net_value']==20 and result['total_cost']==10
 assert len(result['candidates'])==5

def test_oracle_all_negative_selects_nobody():
 c=module('selection_checker');r=c.enumerate_optimum([{'id':'X','cost':1,'net_value':-2}],3,10)
 assert r['selected_ids']==[] and r['expected_net_value']==0

def test_checker_distinguishes_order_null_and_population():
 c=module('selection_checker');e=response();e['selected_ids']=['B','A'];e['effective_k']=2;e['metrics']['recall']=None;e['metrics']['recall_status']='not_identifiable'
 o=json.loads(json.dumps(e));o['selected_ids']=['A','B'];o['metrics']['recall']=0;o['metrics']['population_id']='wrong'
 r=c.evaluate(o,e);assert r['members_match'] and not r['order_match']
 assert 'metrics.recall' in r['mismatches'] and 'metrics.population_id' in r['mismatches']

def test_checker_numeric_tolerance_and_bool_rejection():
 c=module('selection_checker');e=response();o=json.loads(json.dumps(e));o['metrics']['precision']=1-1e-10
 assert c.evaluate(o,e)['metrics_match'];o['metrics']['precision']=True
 assert not c.evaluate(o,e)['metrics_match']

def test_checker_exposes_risk_ranking_separately():
    c=module('selection_checker');e=response();o=json.loads(json.dumps(e));o['risk_ranking_ids']=['B','A']
    r=c.evaluate(o,e)
    assert r['members_match'] and r['order_match'] and not r['ranking_match']
