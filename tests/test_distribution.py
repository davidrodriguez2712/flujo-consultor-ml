import subprocess
import sys
import zipfile
from pathlib import Path


def test_installed_wheel_contains_catalog_and_templates(tmp_path):
    root=Path(__file__).parents[1]
    proc=subprocess.run([sys.executable,'-m','build','--no-isolation','--wheel','--outdir',str(tmp_path)],cwd=root,capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
    wheel=next(tmp_path.glob('*.whl'))
    with zipfile.ZipFile(wheel) as archive:
        names=archive.namelist()
        assert 'acos/resources/catalog.yaml' in names
        assert 'acos/resources/templates/contract.yaml' in names
        assert 'acos/resources/os/workflow/project-lifecycle.md' in names
    script='import sys; sys.path.insert(0,sys.argv[1]); from acos.catalog import load_catalog; assert len(load_catalog().modules)==15; from acos.cli import main; assert main(["--version"])==0'
    proc=subprocess.run([sys.executable,'-I','-c',script,str(wheel)],cwd=tmp_path,capture_output=True,text=True)
    assert proc.returncode==0,proc.stderr
