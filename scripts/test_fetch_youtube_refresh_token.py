import sys
import argparse
from pathlib import Path
from unittest import mock

# Allow importing from repository root
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts import fetch_youtube_refresh_token as fetch_mod



def test_fetch_refresh_token():
    mock_flow = mock.Mock()
    mock_creds = mock.Mock(refresh_token="tok")
    mock_flow.run_console.return_value = mock_creds

    with mock.patch("scripts.fetch_youtube_refresh_token.InstalledAppFlow") as flow_cls:
        flow_cls.from_client_config.return_value = mock_flow
        token = fetch_mod.fetch_refresh_token("id", "secret")

    flow_cls.from_client_config.assert_called_once()
    mock_flow.run_console.assert_called_once_with()
    assert token == "tok"


def test_main(monkeypatch, capsys):
    monkeypatch.setattr(
        fetch_mod.argparse.ArgumentParser,
        "parse_args",
        lambda self: argparse.Namespace(client_id="id", client_secret="secret"),
    )
    monkeypatch.setattr(fetch_mod, "fetch_refresh_token", lambda cid, cs: "tok")

    fetch_mod.main()
    captured = capsys.readouterr()
    assert "REFRESH TOKEN" in captured.out
