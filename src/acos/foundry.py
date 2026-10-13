"""Lee inventario y decisiones; nunca escribe ni ejecuta contenido Foundry."""
from dataclasses import dataclass, field
from pathlib import Path
import hashlib
import json
import re
from .contracts import Finding, UserConfig, valid_slug
from .yaml_io import parse_yaml

STATUSES={'experimental','evaluated','validated','stable'}

@dataclass
class SkillRecord:
    name: str
    status: str
    version: str
    source_ref: str
    local_root: Path
    files: list[dict]
    tree_sha256: str
    limits: str
    dependencies: list[str]
    decision: str | None

@dataclass
class FoundryInventory:
    root: Path | None
    skills: list[SkillRecord] = field(default_factory=list)
    findings: list[Finding] = field(default_factory=list)


def discover_foundry(config: UserConfig, candidates: list[Path]) -> Path | None:
    if config.foundry_path:
        return Path(config.foundry_path).expanduser()
    return next((p for p in candidates if p.is_dir()),None)


def hash_bundle(root: Path) -> tuple[str,list[dict]]:
    if root.is_symlink(): raise ValueError('Bundle symlink no permitido')
    result=[]
    for path in sorted(root.rglob('*')):
        if path.is_symlink(): raise ValueError('Recurso symlink no permitido')
        if path.is_file():
            rel=path.relative_to(root).as_posix()
            result.append({'relative_path':rel,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    encoded=json.dumps([(x['relative_path'],x['sha256']) for x in result],ensure_ascii=False,separators=(',',':')).encode()
    return hashlib.sha256(encoded).hexdigest(),result


def frontmatter(path: Path) -> tuple[dict,str]:
    content=path.read_text(encoding='utf-8')
    match=re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)(.*)',content,re.S)
    if not match: raise ValueError('Frontmatter ausente')
    return parse_yaml(match[1]),match[2]


def candidate_decisions(root: Path) -> dict[str,list[str]]:
    result={}
    folder=root/'candidates'
    if folder.is_symlink(): return result
    for path in sorted(folder.glob('*')):
        if not path.is_file() or path.is_symlink(): continue
        try:
            meta,body=frontmatter(path)
            name=meta.get('name')
            if not isinstance(name,str): continue
            # Only an explicitly named/id-matched record can veto an operational skill.
            if meta.get('id') not in (name,'acos-'+name): continue
            section=re.search(r'^# Decisión\s*\n(.*?)(?=^# |\Z)',body,re.M|re.S)
            decision=re.search(r'Estado:\s*\*\*([^*]+)\*\*',section[1]) if section else None
            result.setdefault(name,[]).append(decision[1].strip().lower() if decision else 'ambiguous')
        except (ValueError,OSError,UnicodeError): continue
    return result


def scan_foundry(root: Path | None) -> FoundryInventory:
    inventory=FoundryInventory(root)
    if root is None or not root.is_dir():
        inventory.findings.append(Finding(code='foundry-missing',message='Foundry no disponible; continuar con pautas OS y gaps.'))
        return inventory
    if root.is_symlink():
        inventory.findings.append(Finding(code='foundry-symlink',message='Foundry symlink no permitido.'))
        return inventory
    decisions=candidate_decisions(root)
    for folder in [root/'experiments'/'skills',root/'stable']:
        if any(p.is_symlink() for p in [folder,folder.parent]):
            inventory.findings.append(Finding(code='unsafe-root',message='Raíz operativa symlink excluida.'));continue
        for path in sorted(folder.glob('*/SKILL.md')):
            try:
                meta,body=frontmatter(path)
                name=valid_slug(meta['name']);nested=meta.get('metadata') if isinstance(meta.get('metadata'),dict) else {};status=meta['status'] if 'status' in meta else nested['status'];version=meta['version'] if 'version' in meta else nested['version']
                if path.parent.name!=name or status not in STATUSES or not isinstance(version,str) or not re.fullmatch(r'\d+\.\d+\.\d+',version):
                    raise ValueError('Metadata incompatible')
                recorded=decisions.get(name,[])
                if any(d not in {'experimentar','experimental','evaluated','validated','stable'} for d in recorded):
                    inventory.findings.append(Finding(code='decision-excluded',message=f'{name}: decisión no operativa o ambigua.'));continue
                tree,filelist=hash_bundle(path.parent)
                requires=meta.get('requires',[])
                if not isinstance(requires,list) or any(not isinstance(x,str) for x in requires):raise ValueError('requires inválido')
                # Relative Markdown links are execution dependencies only when not a provenance reference.
                missing=[]
                for label,target in re.findall(r'\[([^\]]+)\]\(([^)]+)\)',body):
                    if target.startswith(('http:','https:','#')): continue
                    target=target.split('#')[0]
                    if any(w in label.lower() for w in ['origen','procedencia','candidate','foundry']):continue
                    resolved=(path.parent/target).resolve()
                    if not resolved.is_relative_to(path.parent.resolve()) or not resolved.exists(): missing.append(target)
                inventory.skills.append(SkillRecord(name,status,version,'foundry:'+path.parent.relative_to(root).as_posix(),path.parent,filelist,tree,body[:1800],requires+missing,'; '.join(recorded) or None))
            except (ValueError,KeyError,TypeError,OSError,UnicodeError) as exc:
                inventory.findings.append(Finding(code='invalid-skill',message=f'{path.parent.name}: {exc}'))
    counts={name:sum(s.name==name for s in inventory.skills) for name in {s.name for s in inventory.skills}}
    duplicates={name for name,n in counts.items() if n>1}
    inventory.skills=[s for s in inventory.skills if s.name not in duplicates]
    for name in sorted(duplicates): inventory.findings.append(Finding(code='duplicate-skill',message=f'{name}: múltiples fuentes; resolver conflicto.'))
    return inventory
