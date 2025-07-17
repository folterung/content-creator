#!/usr/bin/env python3
"""Generate a content project based on trending news topics."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path
import urllib.request
import xml.etree.ElementTree as ET

from generate_content import create_project


def fetch_trending_topics() -> list[str]:
    """Return a list of trending news topics in the US."""
    url = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = resp.read()
    except Exception as exc:  # pragma: no cover - network may fail
        print(f"Failed to fetch trending topics: {exc}")
        return []

    root = ET.fromstring(data)
    return [item.findtext("title") for item in root.findall("./channel/item")]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gather trending topics and create a project folder",
    )
    parser.add_argument(
        "topic",
        nargs="?",
        default="Trending topics",
        help="Optional topic to include in the project",
    )
    args = parser.parse_args()

    slug = datetime.now().strftime("%Y-%m-%d")
    project_dir = create_project(slug)

    topics = fetch_trending_topics()

    references = project_dir / "references.md"
    references.write_text(f"Sources gathered about {args.topic}\n")

    manuscript = project_dir / "manuscript.md"
    manuscript_lines = ["# Trending Topics", ""]
    if topics:
        manuscript_lines += [f"- {t}" for t in topics]
    else:
        manuscript_lines.append("No trending topics found.")
    manuscript.write_text("\n".join(manuscript_lines))

    timestamps = project_dir / "video_timestamps.txt"
    ts_lines = []
    for idx, title in enumerate(topics, start=0):
        ts_lines.append(f"00:{idx:02d}:00 - {title}")
    timestamps.write_text("\n".join(ts_lines))

    print(f"Project created at {project_dir}")


if __name__ == "__main__":
    main()
