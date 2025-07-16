import sys
import argparse
from datetime import datetime
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import generate_project as gp


def test_fetch_trending_topics(monkeypatch):
    sample_rss = """
    <rss><channel>
        <item><title>Topic1</title></item>
        <item><title>Topic2</title></item>
    </channel></rss>
    """

    class DummyResp:
        def __init__(self, text):
            self.text = text.encode()
        def read(self):
            return self.text
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc, tb):
            pass

    monkeypatch.setattr(gp.urllib.request, "urlopen", lambda *a, **k: DummyResp(sample_rss))
    topics = gp.fetch_trending_topics()
    assert topics == ["Topic1", "Topic2"]


def test_main_creates_files(monkeypatch, tmp_path):
    monkeypatch.setattr(gp, "fetch_trending_topics", lambda: ["A", "B"])
    monkeypatch.setattr(gp, "create_project", lambda slug: tmp_path)
    monkeypatch.setattr(
        gp.argparse.ArgumentParser,
        "parse_args",
        lambda self: argparse.Namespace(topic="t"),
    )
    gp.main()
    assert (tmp_path / "manuscript.md").exists()
    assert (tmp_path / "video_timestamps.txt").exists()
