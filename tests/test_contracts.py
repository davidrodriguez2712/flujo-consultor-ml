import pytest
from pydantic import ValidationError
from acos.contracts import ProjectProfile
from acos.yaml_io import read_yaml, write_yaml_bytes
from acos.config import validate_slug


def test_profile_schema_roundtrip(tmp_path):
    p = ProjectProfile(project={'slug': 'fraude', 'name': 'Fraude'})
    path = tmp_path / 'profile.yaml'
    path.write_bytes(write_yaml_bytes(p))
    assert ProjectProfile.model_validate(read_yaml(path)) == p


def test_duplicate_yaml_key_rejected(tmp_path):
    p = tmp_path / 'bad.yaml'; p.write_text('name: a\nname: b\n')
    with pytest.raises(ValueError): read_yaml(p)


def test_unknown_schema_rejected():
    with pytest.raises(ValidationError): ProjectProfile(schema_version=2, project={'slug':'ok','name':'Ok'})


def test_unknown_fields_rejected():
    with pytest.raises(ValidationError): ProjectProfile(project={'slug':'ok','name':'Ok'}, typo=True)


def test_missing_business_fields_remain_null():
    p = ProjectProfile(project={'slug':'ok','name':'Ok'})
    assert p.engagement.decision is None and p.data.characteristics == {}


@pytest.mark.parametrize('name', ['CON','NUL','con.txt','..','a/b','a\\b','/tmp/a','a.','aux','a'*65])
def test_unsafe_slug_windows_reserved(name):
    with pytest.raises(ValueError): validate_slug(name)
