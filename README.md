# 📹 Content Creator

A modular, Codex-powered content creation pipeline: from trusted-news gathering to video production and automatic YouTube publishing.

---

## 🚀 Features

* `!generate <date>`:

  * Fetches credible news from reliable sources (e.g. Reuters, AP, NYT).
  * Filters for high-quality headlines.
  * Saves structured data to `projects/<date>/news.json`.
  * Internally runs `timeline-generator`:

    * Converts news into an ordered video timeline.
    * Defines segments with timestamps, voiceover scripts, visuals, cues.
    * Outputs `projects/<date>/video_timeline.json`.

* `!produce <date>`:

  * Parses `video_timeline.json`.
  * Retrieves or generates assets (images, clips, TTS voiceover).
  * Applies transitions, text overlays, and background audio.
  * Compiles and renders a complete video.
  * Uploads the final video to YouTube via API.
  * Generates a summary metadata file:

    * `projects/<date>/video_metadata.json` (YouTube link, video ID, duration, segment data)

---

## 📂 Project Structure

```
content-creator/
├── AGENTS.md             ← Codex agent specs for generate/produce
├── README.md            ← This overview
├── requirements.txt     ← Add dependencies here
├── scripts/             ← Custom helper scripts (e.g., for TTS, asset-fetching)
├── tests/               ← Unit tests (pytest)
└── projects/
    └── YYYY-MM-DD/
        ├── news.json
        ├── video_timeline.json
        └── video_metadata.json
```

---

## 🛠 Getting Started

1. Ensure `AGENTS.md` exists and Codex is configured to run against this repo.

2. Add any required dependencies to `requirements.txt` & run:

   ```bash
   pip install -r requirements.txt
   ```

3. Initiate content generation via Codex:

   ```bash
   !generate today
   ```

   * Creates `projects/2025-07-17/news.json`
   * Then produces `projects/2025-07-17/video_timeline.json`

4. Render and publish the video:

   ```bash
   !produce today
   ```

   * Produces a rendered video
   * Uploads the video to YouTube
   * Creates `video_metadata.json` with YouTube video ID and summary info

5. Run tests:

   ```bash
   pytest
   ```

---

## 📋 agents.md Overview

* `news-collector`: fetches/filters news → `news.json`
* `timeline-generator`: transforms news into timeline → `video_timeline.json`
* `video-producer`: renders visuals/audio, uploads video → YouTube + `video_metadata.json`

Each agent is invoked based on commands (`!generate`, `!produce`), guiding Codex with minimal prompting. See `AGENTS.md` for full specs.

---

## ✅ Testing & Quality

* Use pytest to validate JSON formats and script logic.
* Ensure news is properly filtered—no low-credibility sources.
* Validate video timeline structure (timestamps, voiceover segments).
* Confirm final video uploads successfully and metadata reflects accurate information.

---

## 🤝 Contributing

* Add or adjust trusted news sources in `news-collector`.
* Improve scripts under `scripts/` (e.g., better asset sourcing, YouTube uploader).
* Submit test cases in `tests/` to cover edge cases.
* Pull requests and issues welcome.

---

## 🔗 About

This repository establishes a strong foundation for automated, agent-driven content pipelines. Blend it with your Codex-powered agents—or replace any step with preferred tools (e.g., custom TTS, cloud rendering).

---

## 📞 Contact

For setup questions or collaboration, feel free to open an issue.

---

*Ready to build your daily news-to-video engine?* Hit `!generate` and let it do the rest—all the way to YouTube.
