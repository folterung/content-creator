#!/usr/bin/env python3
"""Generate a complete content project from research to video upload."""

from __future__ import annotations

import argparse
from datetime import datetime
from pathlib import Path

from generate_content import create_project


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the full content creation pipeline for a topic"
    )
    parser.add_argument("topic", help="Topic to research and generate content about")
    args = parser.parse_args()

    slug = datetime.now().strftime("%Y%m%d-%H%M%S")
    project_dir = create_project(slug)

    references = project_dir / "references.md"
    references.write_text(f"Sources gathered about {args.topic}\n")

    manuscript = project_dir / "manuscript.md"
    manuscript.write_text(
        f"# Manuscript about {args.topic}\n\nThis document cites sources listed in references.md."
    )

    video_script = project_dir / "video_script.md"
    video_script.write_text(
        "Screen by screen breakdown aligned with the manuscript for Sora video generation."
    )

    video_file = project_dir / "output.mp4"
    video_file.touch()

    print(f"Generated video placeholder at {video_file}")
    print(f"Would upload {video_file} to YouTube using upload_to_youtube.py")
    print(f"Project created at {project_dir}")


if __name__ == "__main__":
    main()
