#!/usr/bin/env python3
"""Produce a video from a timeline and upload it to YouTube."""
from __future__ import annotations

import argparse
import json
import subprocess
from datetime import datetime
from pathlib import Path

from upload_to_youtube import get_authenticated_service, upload_video


def load_timeline(date: str) -> dict:
    """Load timeline JSON for the given date."""
    path = Path("projects") / date / "video_timeline.json"
    if not path.exists():
        raise FileNotFoundError(f"Missing timeline file: {path}")
    return json.loads(path.read_text())


def render_placeholder_video(timeline: dict, output_path: Path) -> Path:
    """Render a placeholder video using ffmpeg."""
    segments = timeline.get("segments", [])
    duration = max(len(segments) * 30, 1)
    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "lavfi",
        "-i",
        f"color=c=blue:s=1280x720:d={duration}",
        "-c:v",
        "libx264",
        "-t",
        str(duration),
        "-pix_fmt",
        "yuv420p",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


def save_metadata(date: str, response: dict, segments: int) -> Path:
    """Save upload metadata to the project directory."""
    project_dir = Path("projects") / date
    project_dir.mkdir(parents=True, exist_ok=True)
    meta_path = project_dir / "video_metadata.json"
    metadata = {
        "youtube_video_id": response.get("id"),
        "url": f"https://youtube.com/watch?v={response.get('id')}",
        "duration": response.get("duration"),
        "segments": segments,
        "upload_timestamp": datetime.utcnow().isoformat() + "Z",
    }
    meta_path.write_text(json.dumps(metadata, indent=2))
    return meta_path


def main(date: str | None = None) -> Path:
    if date is None:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    timeline = load_timeline(date)
    project_dir = Path("projects") / date
    project_dir.mkdir(parents=True, exist_ok=True)
    video_path = project_dir / "output.mp4"
    render_placeholder_video(timeline, video_path)

    service = get_authenticated_service()
    response = upload_video(service, video_path, f"Daily News {date}", "", [])
    return save_metadata(date, response, len(timeline.get("segments", [])))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Produce and upload video")
    parser.add_argument("date", nargs="?", help="Date to produce (YYYY-MM-DD)")
    args = parser.parse_args()
    main(args.date)
