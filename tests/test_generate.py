import sys
import argparse
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from scripts import generate_content as gen_mod


def test_create_project(tmp_path):
    path = gen_mod.create_project(tmp_path / 'demo')
    assert (path / 'ideas.md').exists()
    assert (path / 'references.md').exists()
    assert (path / 'manuscript.md').exists()
    assert (path / 'video_script.md').exists()


def test_main(monkeypatch, capsys, tmp_path):
    monkeypatch.setattr(
        gen_mod.argparse.ArgumentParser,
        "parse_args",
        lambda self: argparse.Namespace(slug=str(tmp_path / "demo")),
    )
    gen_mod.main()
    captured = capsys.readouterr()
    assert "Created project" in captured.out

