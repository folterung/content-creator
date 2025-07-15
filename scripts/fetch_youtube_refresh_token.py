"""Fetch a YouTube OAuth refresh token using the installed app flow."""

import argparse
from google_auth_oauthlib.flow import InstalledAppFlow

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
AUTH_URI = "https://accounts.google.com/o/oauth2/auth"
TOKEN_URI = "https://oauth2.googleapis.com/token"


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

    flow = InstalledAppFlow.from_client_config(
        {
            "installed": {
                "client_id": args.client_id,
                "client_secret": args.client_secret,
                "auth_uri": AUTH_URI,
                "token_uri": TOKEN_URI,
            }
        },
        scopes=[YOUTUBE_UPLOAD_SCOPE],
    )

    creds = flow.run_console()
    print("\nREFRESH TOKEN:\n", creds.refresh_token)


if __name__ == "__main__":
    main()
