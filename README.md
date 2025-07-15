# Content Creator

This repository provides a starting point for building an automated content creation workflow. The project uses the Codex platform to coordinate tasks such as brainstorming ideas, gathering references, writing manuscripts, and optionally generating video output.

The repository is intentionally lightweight. Custom scripts can be placed under `scripts/` and content for each project lives in `projects/`.

## Getting Started

1. Ensure the `AGENTS.md` file is present at the repository root. It outlines agent instructions for automated workflows.
2. When new content is requested, run your Codex instance with this repository to generate the necessary files under `projects/`.
3. Add new dependencies in `requirements.txt` if needed and update tests.

Run tests using:

```
pytest
```


