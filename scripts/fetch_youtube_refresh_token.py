"""Fetch a YouTube OAuth refresh token using the installed app flow."""

import argparse
from google_auth_oauthlib.flow import InstalledAppFlow

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"


def fetch_refresh_token(client_id: str, client_secret: str) -> str:
    """Run the OAuth flow and return the refresh token."""
    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": client_id,
                "client_secret": client_secret,
                "auth_uri": AUTH_URI,
                "token_uri": TOKEN_URI,
            }
        },
        scopes=[YOUTUBE_UPLOAD_SCOPE],
    )

    creds = flow.run_console()
    return creds.refresh_token


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch a YouTube refresh token via OAuth 2.0"
    )
    parser.add_argument("--client-id", required=True, help="OAuth client ID")
    parser.add_argument(
        "--client-secret",
        required=True,
        help="OAuth client secret",
    )
    args = parser.parse_args()

    token = fetch_refresh_token(args.client_id, args.client_secret)
    print("\nREFRESH TOKEN:\n", token)


if __name__ == "__main__":
    main()
