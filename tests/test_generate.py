import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts.generate_content import create_project


def test_create_project(tmp_path):
    path = create_project(tmp_path / 'demo')
    assert (path / 'ideas.md').exists()
    assert (path / 'references.md').exists()
    assert (path / 'manuscript.md').exists()
    assert (path / 'video_script.md').exists()

