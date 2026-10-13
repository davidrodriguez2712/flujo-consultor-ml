from pathlib import Path
import os
import tempfile
from platformdirs import user_config_path
from .contracts import UserConfig, valid_slug
from .yaml_io import read_yaml, write_yaml_bytes

validate_slug = valid_slug


def config_location() -> Path:
    return user_config_path('acos') / 'config.yaml'


def load_config(config_path: Path | None = None) -> UserConfig:
    path=config_path or config_location()
    return UserConfig.model_validate(read_yaml(path)) if path.exists() else UserConfig()


def save_config(config: UserConfig, config_path: Path | None = None) -> None:
    path=config_path or config_location()
    path.parent.mkdir(parents=True,exist_ok=True)
    fd,name=tempfile.mkstemp(dir=path.parent,prefix='.acos-config-')
    try:
        with os.fdopen(fd,'wb') as out: out.write(write_yaml_bytes(config))
        os.replace(name,path)
    finally:
        Path(name).unlink(missing_ok=True)
