# AGENTS.md

This file defines the agents used in the `content-creator` pipeline. Each agent automates a distinct step in the content production process.

Commands like `!generate <date>` and `!produce <date>` **must be interpreted as execution requests**, not requests to generate or modify code.

All generated files are saved in: `projects/<date>/`

---

## 🎯 Command Overview

| Command          | Step-by-Step Workflow                                      | Output Files                          |
|------------------|-------------------------------------------------------------|----------------------------------------|
| `!generate DATE` | ① `news-collector` → ② `timeline-generator`                | `news.json`, `video_timeline.json`     |
| `!produce DATE`  | ③ `video-producer`                                         | `video_metadata.json`, YouTube upload  |

---

## ✅ Agent Details

---

### 📰 Agent: `news-collector`

**Command Trigger:** `!generate <date>`

**Description:** Collects high-quality news articles from trusted sources for the given date.

#### Responsibilities:

- Default to today’s date if no date is supplied.
- Fetch news from sources like Reuters, AP, NYT.
- Filter out untrustworthy or irrelevant headlines.
- Save output to: `projects/<date>/news.json`

#### Output Example:

```json
{
  "date": "2025-07-17",
  "headlines": [
    {
      "title": "Tech Stocks Rally Amid Earnings Reports",
      "summary": "Major tech firms outperformed earnings expectations.",
      "source": "Reuters",
      "url": "https://reuters.com/...",
      "timestamp": "2025-07-17T08:00:00Z"
    }
  ]
}
