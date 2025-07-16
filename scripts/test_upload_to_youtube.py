import sys
from pathlib import Path
from unittest import mock

sys.path.append(str(Path(__file__).resolve().parents[1]))

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
