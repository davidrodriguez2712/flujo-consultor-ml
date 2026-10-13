"""Checker de formato/estado/referencias; nunca sustituye revisión semántica."""
import argparse,json,math
from pathlib import Path

CHECKER_VERSION='0.1.0'
STATUSES={'READY','MUST_CORRECT','NOT_DETERMINABLE'}


def unique_object(pairs):
    obj={}
    for key,value in pairs:
        if key in obj:raise ValueError('Clave duplicada')
        obj[key]=value
    return obj


def reject_constant(value):
    raise ValueError('Número no finito')


def finite_float(value):
    result=float(value)
    if not math.isfinite(result):raise ValueError('Número no finito')
    return result


def strings(value):
    return isinstance(value,list) and all(isinstance(v,str) for v in value)


def conforms(obj):
    if not isinstance(obj,dict) or not isinstance(obj.get('status'),str) or obj['status'] not in STATUSES:return False
    if not isinstance(obj.get('next_step'),str):return False
    if not all(strings(obj.get(k)) for k in ('proposed_actions','limitations')):return False
    findings=obj.get('findings')
    if not isinstance(findings,list):return False
    return all(isinstance(f,dict) and isinstance(f.get('statement'),str) and strings(f.get('evidence_paths')) for f in findings)


def check_text(text,expected,artifact_paths):
    result={'checker_version':CHECKER_VERSION,'strict_json_pass':False,'schema_pass':False,'status_matches':None,'references_exist':None,'unknown_references':[],'semantic_review':'NOT_RUN','overall_content_pass':None}
    try:
        obj=json.loads(text,object_pairs_hook=unique_object,parse_constant=reject_constant,parse_float=finite_float)
        # También rechazar strings que no son UTF-8 válidos, conservando input externo.
        json.dumps(obj,ensure_ascii=False).encode('utf-8')
    except (ValueError,TypeError,UnicodeError,RecursionError):return result
    result['strict_json_pass']=True
    if not conforms(obj):return result
    result['schema_pass']=True
    result['status_matches']=obj['status']==expected['status']
    refs={path for finding in obj['findings'] for path in finding['evidence_paths']}
    result['unknown_references']=sorted(refs-set(artifact_paths))
    result['references_exist']=not result['unknown_references']
    result['referenced_paths']=sorted(refs)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result_text',type=Path)
    parser.add_argument('expected',type=Path)
    parser.add_argument('artifacts',type=Path)
    args=parser.parse_args()
    result=check_text(args.result_text.read_text(encoding='utf-8'),json.loads(args.expected.read_text()),list(json.loads(args.artifacts.read_text())))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    # Exit 0 certifica únicamente checks deterministas, nunca semántica completa.
    raise SystemExit(0 if all(result[k] is True for k in ('strict_json_pass','schema_pass','status_matches','references_exist')) else 4)
