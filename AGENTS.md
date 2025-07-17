# agents.md

## Overview

This document defines the Codex-accessible agents used in the `content-creator` project. Each agent handles a specific phase of the pipeline and is invoked using a natural-language command such as `!generate today` or `!produce today`. Outputs are saved in structured JSON formats under the `projects/<date>/` directory.

Codex should treat each command as an orchestrated task, following these responsibilities and file contracts.

---

## Agent: `news-collector`

**Trigger:** `!generate <date>`

**Role:** Collect relevant, high-quality news data from trusted sources.

### Responsibilities:

* Determine the target date (default to today if not supplied).
* Query verified, reputable news feeds (e.g., Reuters, AP, NYT).
* Filter out low-credibility or clickbait content.
* Extract top stories with summaries, links, timestamps.
* Output data to: `projects/<date>/news.json`

### Output Example:

```json
{
  "date": "2025-07-17",
  "headlines": [
    {
      "title": "Global Markets Surge on Tech Earnings",
      "summary": "Tech stocks drive global indices higher after strong quarterly results.",
      "source": "Reuters",
      "url": "https://reuters.com/...",
      "timestamp": "2025-07-17T09:00:00Z"
    }
  ]
}
```

---

## Agent: `timeline-generator`

**Trigger:** Automatically invoked after `news-collector` completes.

**Role:** Create a video storyboard (timeline) from the collected news data.

### Responsibilities:

* Read `projects/<date>/news.json`.
* Create one timeline segment per headline.
* Include: start/end times, voiceover narration, visual cue suggestions.
* Output to: `projects/<date>/video_timeline.json`

### Output Example:

```json
{
  "segments": [
    {
      "start": "00:00",
      "end": "00:30",
      "headline": "Markets Surge on Tech News",
      "description": "Charts and footage of Wall Street, tech companies, and stock tickers.",
      "visual_cues": ["stock charts", "b-roll office scenes"],
      "voiceover": "Markets surged today as major tech companies posted better-than-expected earnings..."
    }
  ]
}
```

---

## Agent: `video-producer`

**Trigger:** `!produce <date>`

**Role:** Generate a complete video and upload it to YouTube.

### Responsibilities:

* Read `projects/<date>/video_timeline.json`.
* Retrieve or synthesize:

  * Visual assets (stock footage, images)
  * Voiceover narration (TTS or pre-recorded)
  * Background music or ambient sound
* Render the full video.
* Upload the video to YouTube using pre-authorized API credentials.
* Store metadata in `projects/<date>/video_metadata.json`.

### Output Example:

```json
{
  "youtube_video_id": "AbCdEfGhIjK",
  "url": "https://youtube.com/watch?v=AbCdEfGhIjK",
  "duration": "3:45",
  "segments": 5,
  "upload_timestamp": "2025-07-17T11:00:00Z"
}
```

---

## Summary

| Command          | Agents Involved                        | Output Files                          |
| ---------------- | -------------------------------------- | ------------------------------------- |
| `!generate DATE` | `news-collector`, `timeline-generator` | `news.json`, `video_timeline.json`    |
| `!produce DATE`  | `video-producer`                       | YouTube upload, `video_metadata.json` |

---

Ensure Codex chains agent operations sequentially and verifies file existence before moving to the next phase. Fail gracefully if expected inputs are missing.

For future extension: consider agents like `comment-responder` (automated replies), `trend-analyzer`, or `performance-reporter`.
