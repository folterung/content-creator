# Codex Agent Instructions

These instructions apply to the entire repository.

## Purpose
Provide an automated workflow for generating content. The agent can brainstorm ideas, gather reference articles, draft manuscripts, and optionally create accompanying videos.

## Repository Structure
- `projects/` - one subfolder per content project. The agent creates a new timestamped or slugged folder when starting a project.
- `scripts/` - automation scripts. The agent can create or update tools here.

## Workflow Guidance
1. **Idea Generation**
   - When given a high-level topic, create a list of content ideas.
   - Store generated ideas in `projects/<slug>/ideas.md`.

2. **Research**
   - For the chosen idea, gather references from reputable sources. Save notes in `projects/<slug>/references.md`.

3. **Manuscript**
   - Draft a manuscript in `projects/<slug>/manuscript.md`. Include sections such as introduction, main discussion, and conclusion.

4. **Video Creation**
   - If video output is requested, create a script in `projects/<slug>/video_script.md`.
   - The agent may integrate with video generation tools such as Sora if available.

5. **Committing Work**
   - After completing a step, commit new files or changes.
   - If network access blocks a request, note it in the PR description under "Network access".

## Testing
- If the repository contains a `tests/` directory, run `pytest` after changes.
- Otherwise run `echo 'No tests'`.

