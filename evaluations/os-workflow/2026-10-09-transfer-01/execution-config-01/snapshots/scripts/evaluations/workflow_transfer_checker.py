"""Checks estructurales de transferencia; jamás aprueba contenido o gates."""
import argparse
import importlib.util
import json
from pathlib import Path
import re

VERSION='0.1.0'
HEADINGS=['Estado','Hallazgos','Acciones propuestas','Siguiente paso','Límites']
STATUSES={'READY','MUST_CORRECT','NOT_DETERMINABLE'}
# Rutas locales de los fixtures, en texto, inline code o destinos Markdown.
PATH_PATTERN=re.compile(r'(?<![\w./-])([\w.-]+(?:/[\w.-]+)+\.(?:json|md))(?![\w./-])')


def check_text(text,expected,artifact_paths):
    requested=expected.get('format','json')
    if requested=='json':
        spec=importlib.util.spec_from_file_location('workflow_output_checker',Path(__file__).with_name('workflow_output_checker.py'))
        checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
        result=checker.check_text(text,expected,artifact_paths)
        result.update(transfer_checker_version=VERSION,format='json',format_pass=result['schema_pass'],
                      references_present=bool(result.get('referenced_paths')))
        return result
    if requested!='markdown':raise ValueError('Formato de transferencia no admitido')
    result={'transfer_checker_version':VERSION,'format':'markdown','format_pass':False,
            'strict_json_pass':None,'schema_pass':None,'status_matches':None,
            'references_exist':None,'references_present':False,'unknown_references':[],
            'semantic_review':'NOT_RUN','overall_content_pass':None}
    try:text.encode('utf-8')
    except UnicodeError:return result
    sections=[];title=None;body=[];fence=None
    for line in text.splitlines():
        stripped=line.strip()
        opening=re.match(r'^[ ]{0,3}(`{3,}|~{3,})(.*)$',line)
        if fence:
            body.append(line)
            if re.fullmatch(r'[ ]{0,3}'+re.escape(fence[0])+r'{'+str(fence[1])+r',}[ \t]*',line):fence=None
            continue
        if opening:
            if title is None:return result  # Memo envuelto en fences o prefacio.
            fence=(opening.group(1)[0],len(opening.group(1)));body.append(line);continue
        heading=re.match(r'^[ ]{0,3}(#{1,6})[ \t]+(.+?)\s*$',line)
        if heading:
            label=re.sub(r'[ \t]+#+[ \t]*$','',heading.group(2)).strip()
            if len(heading.group(1))!=2:return result
            if title is not None:sections.append((title,'\n'.join(body).strip()))
            title=label;body=[]
        elif title is None:
            if stripped:return result
        else:body.append(line)
    if fence or title is None:return result
    sections.append((title,'\n'.join(body).strip()))
    if [name for name,_ in sections]!=HEADINGS or any(not content for _,content in sections):return result
    state=sections[0][1]
    # Interpretar énfasis Markdown sin modificar ni reescribir el raw.
    for marker in ('**','__','`','*','_'):
        if state.startswith(marker) and state.endswith(marker):
            state=state[len(marker):-len(marker)];break
    if state not in STATUSES:return result
    result.update(format_pass=True,status_matches=state==expected['status'],observed_status=state)
    refs=sorted(set(PATH_PATTERN.findall(sections[1][1])))
    unknown=sorted(set(refs)-set(artifact_paths))
    result.update(referenced_paths=refs,references_present=bool(refs),
                  unknown_references=unknown,references_exist=not unknown)
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('result_text',type=Path);parser.add_argument('expected',type=Path);parser.add_argument('artifacts',type=Path)
    args=parser.parse_args()
    result=check_text(args.result_text.read_text(encoding='utf-8'),json.loads(args.expected.read_text()),list(json.loads(args.artifacts.read_text())))
    print(json.dumps(result,ensure_ascii=False,indent=2))
    # Exit0 son solo checks deterministas; ausencia de soporte queda revisión semántica.
    raise SystemExit(0 if all(result[k] is True for k in ('format_pass','status_matches','references_exist')) else 4)
