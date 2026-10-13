import pytest
from acos.config import load_config, save_config, config_location
from acos.contracts import UserConfig


def test_config_path_separate_from_project(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert config_location().parent != tmp_path
    p = tmp_path/'preferences'/'config.yaml'
    save_config(UserConfig(foundry_path='/foundry'), p)
    assert load_config(p).foundry_path == '/foundry'


def test_config_invalid_does_not_get_overwritten(tmp_path):
    p=tmp_path/'config.yaml'; p.write_text('schema_version: 9\n')
    with pytest.raises(ValueError): load_config(p)
    assert p.read_text() == 'schema_version: 9\n'
