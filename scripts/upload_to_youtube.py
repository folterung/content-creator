"""Upload a video to YouTube using the YouTube Data API v3."""

import argparse
import os
from pathlib import Path
from typing import List

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Scope required for uploading videos
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
TOKEN_URI = "https://oauth2.googleapis.com/token"


def get_authenticated_service() -> any:
    """Create an authenticated YouTube service using environment variables."""
    client_id = os.environ.get("YOUTUBE_CLIENT_ID")
    client_secret = os.environ.get("YOUTUBE_CLIENT_SECRET")
    refresh_token = os.environ.get("YOUTUBE_REFRESH_TOKEN")

    if not all([client_id, client_secret, refresh_token]):
        raise EnvironmentError(
            "Missing YouTube OAuth credentials in environment variables"
        )

    creds = Credentials(
        token=None,
        refresh_token=refresh_token,
        token_uri=TOKEN_URI,
        client_id=client_id,
        client_secret=client_secret,
        scopes=[YOUTUBE_UPLOAD_SCOPE],
    )
    return build("youtube", "v3", credentials=creds)


def upload_video(
    youtube_service: any,
    video_path: Path,
    title: str,
    description: str,
    tags: List[str] | None = None,
    category: str = "22",
    privacy_status: str = "private",
):
    """Upload the given video file to YouTube."""
    if tags is None:
        tags = []

    body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": str(category),
        },
        "status": {
            "privacyStatus": privacy_status,
        },
    }

    media = MediaFileUpload(str(video_path), resumable=True)
    request = youtube_service.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print("Upload complete")
    return response


def main():
    parser = argparse.ArgumentParser(description="Upload a video to YouTube")
    parser.add_argument("file", type=Path, help="Path to the video file")
    parser.add_argument("--title", help="Video title")
    parser.add_argument("--description", help="Video description", default="")
    parser.add_argument("--tags", nargs="*", default=[], help="Space separated list of tags")
    parser.add_argument(
        "--category", default="22", help="Numeric YouTube video category ID"
    )
    parser.add_argument(
        "--privacy", default="private", choices=["private", "public", "unlisted"],
        help="Initial privacy status"
    )
    args = parser.parse_args()

    if not args.title:
        args.title = args.file.stem

    youtube = get_authenticated_service()
    upload_video(
        youtube,
        args.file,
        args.title,
        args.description,
        args.tags,
        args.category,
        args.privacy,
    )


if __name__ == "__main__":
    main()
