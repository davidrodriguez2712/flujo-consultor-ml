"""YAML seguro, sin claves duplicadas ni timestamps implícitos."""
from pathlib import Path
import yaml
from pydantic import BaseModel
from .contracts import canonical_sha256

class SafeUniqueLoader(yaml.SafeLoader):
    yaml_implicit_resolvers = {k:[(tag,regex) for tag,regex in entries if tag != 'tag:yaml.org,2002:timestamp']
                               for k,entries in yaml.SafeLoader.yaml_implicit_resolvers.items()}


def unique_mapping(loader,node):
    result={}
    for keynode,valnode in node.value:
        key=loader.construct_object(keynode,deep=True)
        if not isinstance(key,str): raise ValueError('Las claves YAML deben ser texto')
        if key in result: raise ValueError(f'Clave YAML duplicada: {key}')
        result[key]=loader.construct_object(valnode,deep=True)
    return result

SafeUniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique_mapping)


def parse_yaml(text: str) -> dict:
    try: data=yaml.load(text,Loader=SafeUniqueLoader)
    except yaml.YAMLError as exc: raise ValueError(f'YAML inválido: {exc}') from exc
    if not isinstance(data,dict): raise ValueError('Se esperaba un objeto YAML')
    return data


def read_yaml(path: Path) -> dict:
    return parse_yaml(path.read_text(encoding='utf-8'))


def write_yaml_bytes(model: BaseModel | dict) -> bytes:
    data=model.model_dump(mode='json') if isinstance(model,BaseModel) else model
    return yaml.safe_dump(data,allow_unicode=True,sort_keys=False).encode('utf-8')
