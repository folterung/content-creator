import sys
from pathlib import Path
from unittest import mock

# Allow importing from repository root
sys.path.append(str(Path(__file__).resolve().parents[1]))

from scripts.fetch_youtube_refresh_token import fetch_refresh_token


def test_fetch_refresh_token():
    mock_flow = mock.Mock()
    mock_creds = mock.Mock(refresh_token="tok")
    mock_flow.run_console.return_value = mock_creds

    with mock.patch("scripts.fetch_youtube_refresh_token.InstalledAppFlow") as flow_cls:
        flow_cls.from_client_config.return_value = mock_flow
        token = fetch_refresh_token("id", "secret")

    flow_cls.from_client_config.assert_called_once()
    mock_flow.run_console.assert_called_once_with()
    assert token == "tok"
