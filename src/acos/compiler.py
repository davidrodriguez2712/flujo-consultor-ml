"""Escritura exclusiva con manifest final y rollback limitado a archivos propios."""
from pathlib import Path, PurePosixPath
import hashlib
import os
import tempfile
import shutil
from . import __version__
from .contracts import Manifest,AcosError,Finding,canonical_sha256,valid_slug
from .foundry import scan_foundry,hash_bundle
from .render import render_project,initial_state
from .yaml_io import write_yaml_bytes


def safe_relative(value: str) -> Path:
    p=PurePosixPath(value)
    if not value or p.is_absolute() or '..' in p.parts or '\\' in value or ':' in value:
        raise AcosError(4,'Ruta de artifact no portable: '+value)
    return Path(*p.parts)


def reject_symlinks(path: Path) -> None:
    for part in [path,*path.parents]:
        if part.is_symlink():raise AcosError(4,'Ruta symlink no permitida: '+str(part))


def target_directory(cwd: Path, slug: str | None, here: bool) -> Path:
    if here and slug is not None:raise AcosError(2,'--here no admite nombre posicional.')
    if here:return cwd
    if slug is None:raise AcosError(2,'Falta nombre de proyecto.')
    return cwd/valid_slug(slug)


def inspect_conflicts(target: Path, files: dict[str,bytes], here: bool) -> list[Finding]:
    reject_symlinks(target)
    if not here and target.exists():return [Finding(code='destination-exists',message='El destino ya existe.',paths=[str(target)])]
    result=[]
    for name in [*files,'.acos/manifest.yaml','.acos/init.lock']:
        path=target/safe_relative(name)
        reject_symlinks(path)
        if path.exists():result.append(Finding(code='file-conflict',message='Archivo existente: '+name,paths=[name]))
        for parent in path.parents:
            if parent==target:break
            if parent.exists() and not parent.is_dir():result.append(Finding(code='parent-conflict',message='Parent no es directorio.',paths=[name]))
    return result


def write_exclusive(path: Path, data: bytes) -> None:
    reject_symlinks(path)
    with path.open('xb') as output:
        try: output.write(data)
        except (OSError,KeyboardInterrupt):
            written=output.tell()
            output.close()
            if not path.is_symlink() and path.read_bytes()==data[:written]:path.unlink()
            raise


def source_check(plan) -> None:
    if not plan.skills:return
    current={s.name:s for s in scan_foundry(plan.foundry_root).skills}
    for old in plan.skills:
        new=current.get(old.name)
        if new is None or (new.tree_sha256,new.status,new.version,new.source_ref,new.decision)!=(old.tree_sha256,old.status,old.version,old.source_ref,old.decision):
            raise AcosError(4,'Foundry cambió después del preview: '+old.name+'; volver a confirmar.')


def compile_project(plan, target: Path, here: bool) -> Manifest:
    if not plan.confirmed:raise AcosError(130,'Composición no confirmada.')
    if plan.selection.profile_sha256!=canonical_sha256(plan.profile):raise AcosError(4,'Perfil cambió después de resolver.')
    source_check(plan)
    content=render_project(plan,initial_state(plan))
    conflicts=inspect_conflicts(target,content,here)
    if conflicts:raise AcosError(4,'Conflictos: '+', '.join(f.message for f in conflicts))
    artifacts=[{'path':name,'ownership':'acos' if name.startswith(('workflow/','playbooks/','.agents/','.claude/')) or name=='AGENTS.md' else 'human','initial_sha256':hashlib.sha256(data).hexdigest()} for name,data in sorted(content.items())]
    snapshots=[]
    for s in plan.skills:
        snapshots.append({'name':s.name,'status':s.status,'version':s.version,'source_ref':s.source_ref,'tree_sha256':s.tree_sha256,'files':s.files,'runtime_paths':[(('.agents/skills/' if r=='codex' else '.claude/skills/')+s.name) for r in plan.profile.runtimes]})
    manifest=Manifest(acos_version=__version__,catalog_version=plan.selection.catalog_version,profile_sha256=canonical_sha256(plan.profile),modules_sha256=canonical_sha256(plan.selection),artifacts=artifacts,skills=snapshots)
    stage=Path(tempfile.mkdtemp(dir=target.parent,prefix='.acos-staging-'))
    created_files=[];created_dirs=[];lock=None
    try:
        for name,data in content.items():
            p=stage/safe_relative(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
        source_check(plan)
        # Exclusive reservation avoids POSIX rename replacing an empty destination created concurrently.
        if not here:target.mkdir();created_dirs.append(target)
        elif not target.is_dir():raise AcosError(4,'--here requiere un directorio existente.')
        def ensure_parent(path):
            missing=[];parent=path.parent
            while not parent.exists():missing.append(parent);parent=parent.parent
            reject_symlinks(path)
            for d in reversed(missing):d.mkdir();created_dirs.append(d)
        lock=target/'.acos/init.lock';ensure_parent(lock)
        lockfd=os.open(lock,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        os.close(lockfd);created_files.append((lock,hashlib.sha256(b'').hexdigest()))
        for name in sorted(content):
            p=target/safe_relative(name);ensure_parent(p)
            data=(stage/safe_relative(name)).read_bytes()
            write_exclusive(p,data)
            created_files.append((p,hashlib.sha256(data).hexdigest()))
        source_check(plan)
        for s in snapshots:
            for rel in s['runtime_paths']:
                if hash_bundle(target/rel)[0]!=s['tree_sha256']:raise AcosError(4,'Snapshot alterado durante copia.')
        p=target/'.acos/manifest.yaml'
        write_exclusive(p,write_yaml_bytes(manifest));created_files.append((p,hashlib.sha256(p.read_bytes()).hexdigest()))
        lock.unlink();created_files=[entry for entry in created_files if entry[0]!=lock]
        return manifest
    except (OSError,ValueError,KeyboardInterrupt) as exc:
        retained=[]
        for p,digest in reversed(created_files):
            try:
                if p.is_symlink() or (digest is not None and p.exists() and hashlib.sha256(p.read_bytes()).hexdigest()!=digest):retained.append(str(p));continue
                p.unlink(missing_ok=True)
            except OSError:retained.append(str(p))
        for d in reversed(created_dirs):
            try:d.rmdir()
            except OSError:
                if d.exists():retained.append(str(d))
        message=f'Inicialización incompleta: {exc}'
        if retained:message+='; reversión incompleta, revisar: '+', '.join(retained)
        raise AcosError(130 if isinstance(exc,KeyboardInterrupt) else 4,message) from exc
    finally:
        shutil.rmtree(stage)
