"""Checker reproducible de la ronda temporal; no ejecuta modelos ni modifica outputs."""
import argparse
import json
from pathlib import Path
import re

FIELDS=('outcome_state_at_extraction','label_availability_at_training','train_eligibility')
ENUMS={FIELDS[0]:{'observed_positive','observed_negative','pending','unknown'},
       FIELDS[1]:{'available','unavailable','indeterminate'},
       FIELDS[2]:{'eligible','exclude','indeterminate'}}

def unique_object(pairs):
    result={}
    for key,value in pairs:
        if key in result:raise ValueError('Clave duplicada: '+key)
        result[key]=value
    return result

def reject_constant(value):
    raise ValueError('Número no finito: '+value)

def parse(text):
    return json.loads(text,object_pairs_hook=unique_object,parse_constant=reject_constant)

def evaluate(text,expected):
    result={'strict_format_pass':False,'diagnostic_parse_used':False,'payload_schema_pass':False,
            'content_evaluable':False,'ids_exact':False,'gate_matches':False,'field_matches':0,'field_total':3*len(expected),
            'row_decisions_correct':0,'row_total':len(expected),'eligible_false_positives':0,
            'valid_rows_excluded':0,'valid_rows_indeterminate':0,'mismatches':[],'row_checks':[]}
    try:
        payload=parse(text);result['strict_format_pass']=True
    except (ValueError,TypeError):
        match=re.fullmatch(r'\s*```(?:json)?\s*\n(.*?)\n```\s*',text,re.S)
        if not match:return result
        try:payload=parse(match.group(1));result['diagnostic_parse_used']=True
        except (ValueError,TypeError):return result
    if not isinstance(payload,dict) or set(payload)!={'rows','open_questions','gate_decision'}:return result
    rows=payload['rows']
    if not isinstance(rows,list):return result
    ids=[row.get('id') for row in rows if isinstance(row,dict)]
    result['ids_exact']=len(ids)==len(rows)==len(expected) and all(isinstance(i,str) for i in ids) and len(set(ids))==len(ids) and set(ids)==set(expected)
    if not result['ids_exact']:return result
    if not isinstance(payload['open_questions'],list) or not all(isinstance(q,str) and q.strip() for q in payload['open_questions']):return result
    if not isinstance(payload['gate_decision'],str):return result
    for row in rows:
        if set(row)!={'id','reason',*FIELDS} or not isinstance(row['reason'],str) or not row['reason'].strip():return result
        if any(not isinstance(row[f],str) or row[f] not in ENUMS[f] for f in FIELDS):return result
    result['payload_schema_pass']=True
    result['content_evaluable']=True
    result['gate_matches']=payload['gate_decision']=='NEEDS_REVIEW'
    for row in rows:
        want=expected[row['id']];checks={'id':row['id']}
        for field in FIELDS:
            checks[field]=row[field]==want[field]
            result['field_matches']+=int(checks[field])
            if not checks[field]:result['mismatches'].append({'id':row['id'],'field':field,'expected':want[field],'actual':row[field]})
        actual=row['train_eligibility'];target=want['train_eligibility']
        result['row_decisions_correct']+=int(actual==target)
        result['eligible_false_positives']+=int(actual=='eligible' and target!='eligible')
        result['valid_rows_excluded']+=int(actual=='exclude' and target=='eligible')
        result['valid_rows_indeterminate']+=int(actual=='indeterminate' and target=='eligible')
        result['row_checks'].append(checks)
    return result

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result',type=Path);parser.add_argument('expected',type=Path)
    args=parser.parse_args()
    print(json.dumps(evaluate(args.result.read_text(),json.loads(args.expected.read_text())['rows']),ensure_ascii=False,indent=2))

if __name__=='__main__':main()
