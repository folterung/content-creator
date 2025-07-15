"""Utility script for triggering content creation tasks."""

import argparse
from pathlib import Path


def create_project(slug: str) -> Path:
    project_dir = Path('projects') / slug
    project_dir.mkdir(parents=True, exist_ok=True)
    (project_dir / 'ideas.md').touch()
    (project_dir / 'references.md').touch()
    (project_dir / 'manuscript.md').touch()
    (project_dir / 'video_script.md').touch()
    return project_dir


def main():
    parser = argparse.ArgumentParser(description="Create a new content project")
    parser.add_argument('slug', help='Folder name for the project')
    args = parser.parse_args()
    project_path = create_project(args.slug)
    print(f"Created project at {project_path}")


if __name__ == '__main__':
    main()
