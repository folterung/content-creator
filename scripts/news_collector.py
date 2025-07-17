"""Collect credible news headlines and output to JSON."""

from __future__ import annotations

import json
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path


CREDIBLE_SOURCES = {
    "Reuters",
    "AP News",
    "Associated Press",
    "The New York Times",
    "BBC",
    "CNN",
    "Los Angeles Times",
    "The Guardian",
}

GOOGLE_NEWS_RSS = "https://news.google.com/rss?hl=en-US&gl=US&ceid=US:en"


def fetch_rss() -> str:
    with urllib.request.urlopen(GOOGLE_NEWS_RSS, timeout=10) as resp:
        return resp.read().decode()


def parse_items(rss_data: str) -> list[dict[str, str]]:
    root = ET.fromstring(rss_data)
    channel = root.find("channel")
    items = []
    for item in channel.findall("item"):
        source_el = item.find("source")
        source = source_el.text if source_el is not None else ""
        if source not in CREDIBLE_SOURCES:
            continue
        title = item.findtext("title") or ""
        link = item.findtext("link") or ""
        pub_date = item.findtext("pubDate") or ""
        description = item.findtext("description") or ""
        items.append({
            "title": title,
            "url": link,
            "timestamp": pub_date,
            "source": source,
            "summary": description,
        })
        if len(items) >= 5:
            break
    return items


def save_news(date: str, items: list[dict[str, str]]) -> Path:
    project_dir = Path("projects") / date
    project_dir.mkdir(parents=True, exist_ok=True)
    news_path = project_dir / "news.json"
    data = {"date": date, "headlines": items}
    news_path.write_text(json.dumps(data, indent=2))
    return news_path


def main(date: str | None = None) -> Path:
    if date is None:
        date = datetime.utcnow().strftime("%Y-%m-%d")
    rss = fetch_rss()
    items = parse_items(rss)
    return save_news(date, items)


if __name__ == "__main__":
    main()
