"""Generate a video timeline from collected news."""

from __future__ import annotations

import json
from datetime import timedelta


def _format_time(td: timedelta) -> str:
    total = int(td.total_seconds())
    h, rem = divmod(total, 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d}"
from pathlib import Path


def load_news(date: str) -> list[dict[str, str]]:
    news_path = Path("projects") / date / "news.json"
    data = json.loads(news_path.read_text())
    return data.get("headlines", [])


def build_timeline(items: list[dict[str, str]]) -> dict:
    segments = []
    start_time = timedelta()
    duration = timedelta(seconds=30)
    for item in items:
        end_time = start_time + duration
        segment = {
            "start": _format_time(start_time),
            "end": _format_time(end_time),
            "headline": item["title"],
            "description": f"Images and footage related to {item['source']}",
            "visual_cues": ["news footage", "relevant images"],
            "voiceover": item["summary"],
        }
        segments.append(segment)
        start_time = end_time
    return {"segments": segments}


def save_timeline(date: str, timeline: dict) -> Path:
    project_dir = Path("projects") / date
    project_dir.mkdir(parents=True, exist_ok=True)
    path = project_dir / "video_timeline.json"
    path.write_text(json.dumps(timeline, indent=2))
    return path


def main(date: str) -> Path:
    items = load_news(date)
    timeline = build_timeline(items)
    return save_timeline(date, timeline)


if __name__ == "__main__":
    import sys
    date = sys.argv[1] if len(sys.argv) > 1 else None
    if date is None:
        from datetime import datetime
        date = datetime.utcnow().strftime("%Y-%m-%d")
    main(date)
