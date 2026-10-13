from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parents[1] / 'src'))
import pytest

@pytest.fixture
def foundry(tmp_path):
    root=tmp_path/'foundry'
    root.mkdir()
    return root


def make_skill(root, name='understand-dataset', status='experimental', folder='experiments/skills'):
    path=root/folder/name
    path.mkdir(parents=True)
    (path/'SKILL.md').write_text(f'---\nname: {name}\nstatus: {status}\nversion: 0.1.0\ndescription: Procedimiento de prueba\n---\n# Límites\nSolo prueba.\n')
    return path
