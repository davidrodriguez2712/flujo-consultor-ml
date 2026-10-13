"""Checks de contenido y enumeración exhaustiva de problemas pequeños de selección."""
import argparse
import itertools
import json
import math
from pathlib import Path

def enumerate_optimum(rows,capacity_k,budget):
    if type(capacity_k) is not int or capacity_k<0:raise ValueError('Capacidad inválida')
    if type(budget) not in (int,float) or not math.isfinite(budget) or budget<0:raise ValueError('Presupuesto inválido')
    rows=[r for r in rows if r.get('eligible',True)]
    if len(rows)>20:raise ValueError('Oracle limitado a 20 registros')
    if len({r['id'] for r in rows})!=len(rows):raise ValueError('IDs duplicados')
    for r in rows:
        if not isinstance(r['id'],str) or not r['id'].strip():raise ValueError('ID inválido')
        for key in ['cost','net_value']:
            if type(r[key]) not in (int,float) or not math.isfinite(r[key]):raise ValueError('Dato numérico inválido')
        if r['cost']<0:raise ValueError('Coste negativo')
    candidates=[]
    for n in range(min(capacity_k,len(rows))+1):
        for subset in itertools.combinations(rows,n):
            cost=sum(r['cost'] for r in subset)
            if cost>budget:continue
            ordered=sorted(subset,key=lambda r:(-r['net_value'],r['id']))
            candidates.append({'selected_ids':[r['id'] for r in ordered],'total_cost':cost,'expected_net_value':sum(r['net_value'] for r in subset)})
    best=min(candidates,key=lambda c:(-c['expected_net_value'],c['total_cost'],sorted(c['selected_ids'])))
    return {**best,'candidates':candidates}

def equal(actual,expected):
    if type(expected) in (int,float):
        return type(actual) in (int,float) and math.isfinite(actual) and abs(actual-expected)<=1e-8
    if expected is None:return actual is None
    return type(actual) is type(expected) and actual==expected

def evaluate(output,expected):
    mismatches=[]
    def check(path,want):
        value=output
        for key in path.split('.'):
            if not isinstance(value,dict) or key not in value:
                mismatches.append(path);return
            value=value[key]
        if not equal(value,want):mismatches.append(path)
    for key in ['output_type','selection_status','eligible_count','capacity_k','effective_k','selected_ids','risk_ranking_ids','total_cost','expected_net_value','feasibility','optimality','gate_decision']:
        check(key,expected[key])
    check('causal_identification.status',expected['causal_identification']['status'])
    # Texto de estimand se revisa semánticamente, no por coincidencia literal.
    for key in ['population_id','precision','recall','lift','precision_status','recall_status','lift_status']:
        check('metrics.'+key,expected['metrics'][key])
    ids=output.get('selected_ids') if isinstance(output,dict) else None
    members_match=isinstance(ids,list) and all(isinstance(i,str) for i in ids) and len(ids)==len(set(ids)) and set(ids)==set(expected['selected_ids'])
    return {'members_match':members_match,'order_match':'selected_ids' not in mismatches,'ranking_match':'risk_ranking_ids' not in mismatches,'capacity_match':not any(k in mismatches for k in ['eligible_count','capacity_k','effective_k']), 'value_match':not any(k in mismatches for k in ['total_cost','expected_net_value']), 'feasibility_match':'feasibility' not in mismatches,'optimality_match':'optimality' not in mismatches,'causal_status_match':'causal_identification.status' not in mismatches,'metrics_match':not any(k.startswith('metrics.') for k in mismatches),'gate_matches':'gate_decision' not in mismatches,'mismatches':mismatches}

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('output',type=Path);parser.add_argument('expected',type=Path);args=parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.output.read_text()),json.loads(args.expected.read_text())),ensure_ascii=False,indent=2))
if __name__=='__main__':main()
