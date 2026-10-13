from pathlib import Path
import pytest
from acos.cli import main
from acos.contracts import ProjectProfile
from acos.yaml_io import write_yaml_bytes


def setup(tmp_path,monkeypatch,answers):
    import acos.cli as cli
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(cli,'load_config',lambda:__import__('acos.contracts',fromlist=['UserConfig']).UserConfig())
    monkeypatch.setattr(cli,'discover_foundry',lambda *args:None)
    values=iter(answers);monkeypatch.setattr('builtins.input',lambda q:next(values))
    p=tmp_path/'profile.yaml';p.write_bytes(write_yaml_bytes(ProjectProfile(project={'slug':'client','name':'Cliente'})))
    return p


def test_profile_file_still_requires_review(tmp_path,monkeypatch):
    p=setup(tmp_path,monkeypatch,['','n'])
    assert main(['init','--profile-file',str(p)])==130
    assert not (tmp_path/'client').exists()


def test_default_init_creates_child(tmp_path,monkeypatch):
    p=setup(tmp_path,monkeypatch,['','s','s'])
    assert main(['init','--profile-file',str(p)])==0
    assert (tmp_path/'client/MANUAL.md').exists()


def test_here_requires_no_positional_name():
    assert main(['init','client','--here'])==2


def test_four_commands_exit_codes(tmp_path,monkeypatch):
    p=setup(tmp_path,monkeypatch,['','s','s'])
    assert main(['init','--profile-file',str(p)])==0
    monkeypatch.chdir(tmp_path/'client')
    assert main(['status'])==0
    assert main(['next'])==0
    assert main(['validate'])==3


def test_cli_eof_cancels_without_writing(tmp_path,monkeypatch):
    p=setup(tmp_path,monkeypatch,[])
    def fail(q):raise EOFError
    monkeypatch.setattr('builtins.input',fail)
    assert main(['init','--profile-file',str(p)])==130
    assert not (tmp_path/'client').exists()


def test_help_is_spanish(capsys):
    assert main(['--help'])==0
    text=capsys.readouterr().out
    assert 'Mostrar esta ayuda' in text and 'Uso:' in text and 'Opciones:' in text
