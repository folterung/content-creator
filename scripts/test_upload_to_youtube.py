import sys
import argparse
import pytest
from pathlib import Path
from unittest import mock

sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import upload_to_youtube as upload_video_module
from scripts.upload_to_youtube import get_authenticated_service, upload_video


def test_get_authenticated_service_uses_refresh_token_env(monkeypatch):
    monkeypatch.setenv("YOUTUBE_CLIENT_ID", "cid")
    monkeypatch.setenv("YOUTUBE_CLIENT_SECRET", "secret")
    monkeypatch.setenv("YOUTUBE_REFRESH_TOKEN", "tok")

    with mock.patch("scripts.upload_to_youtube.build") as build_mock:
        service = get_authenticated_service()

    build_mock.assert_called_once()
    assert service == build_mock.return_value


def test_upload_video(monkeypatch):
    class DummyRequest:
        def __init__(self):
            self.calls = 0
        def next_chunk(self):
            self.calls += 1
            if self.calls == 1:
                class Status:
                    def progress(self):
                        return 0.5
                return Status(), None
            return None, {"id": "123"}

    dummy_insert = mock.Mock(return_value=DummyRequest())
    dummy_videos = mock.Mock(insert=dummy_insert)
    youtube_service = mock.Mock(videos=mock.Mock(return_value=dummy_videos))

    monkeypatch.setattr(
        "scripts.upload_to_youtube.MediaFileUpload",
        lambda *a, **k: mock.Mock(),
    )

    response = upload_video(
        youtube_service,
        Path("/tmp/video.mp4"),
        "title",
        "desc",
        ["t1"],
    )

    assert response == {"id": "123"}
    dummy_insert.assert_called_once()

def test_get_authenticated_service_triggers_oauth(monkeypatch):
    monkeypatch.setenv("YOUTUBE_CLIENT_ID", "cid")
    monkeypatch.setenv("YOUTUBE_CLIENT_SECRET", "secret")
    monkeypatch.delenv("YOUTUBE_REFRESH_TOKEN", raising=False)

    with mock.patch("scripts.upload_to_youtube.fetch_refresh_token", return_value="tok") as fetch_mock, \
         mock.patch("scripts.upload_to_youtube.build") as build_mock:
        service = get_authenticated_service()

    fetch_mock.assert_called_once_with("cid", "secret")
    build_mock.assert_called_once()
    assert service == build_mock.return_value


def test_get_authenticated_service_missing_env(monkeypatch):
    monkeypatch.delenv("YOUTUBE_CLIENT_ID", raising=False)
    monkeypatch.delenv("YOUTUBE_CLIENT_SECRET", raising=False)
    with pytest.raises(EnvironmentError):
        get_authenticated_service()


def test_upload_video_tags_none(monkeypatch):
    dummy_request = mock.Mock()
    dummy_request.next_chunk.side_effect = [(None, {"id": "x"})]
    dummy_insert = mock.Mock(return_value=dummy_request)
    youtube_service = mock.Mock(videos=mock.Mock(return_value=mock.Mock(insert=dummy_insert)))
    monkeypatch.setattr("scripts.upload_to_youtube.MediaFileUpload", lambda *a, **k: mock.Mock())
    response = upload_video(youtube_service, Path("/tmp/v.mp4"), "t", "d", None)
    assert response == {"id": "x"}


def test_main(monkeypatch, tmp_path):
    video = tmp_path / "vid.mp4"
    video.touch()
    monkeypatch.setattr(
        upload_video_module.argparse.ArgumentParser,
        "parse_args",
        lambda self: argparse.Namespace(
            file=video,
            title=None,
            description="desc",
            tags=[],
            category="22",
            privacy="private",
        ),
    )
    dummy_service = mock.Mock()
    monkeypatch.setattr(upload_video_module, "get_authenticated_service", lambda: dummy_service)
    called = {}

    def fake_upload(service, video_path, title, description, tags, category, privacy):
        called.update(
            {
                "service": service,
                "video": video_path,
                "title": title,
                "description": description,
                "tags": tags,
                "category": category,
                "privacy": privacy,
            }
        )

    monkeypatch.setattr(upload_video_module, "upload_video", fake_upload)

    upload_video_module.main()

    assert called["service"] == dummy_service
    assert called["title"] == video.stem
