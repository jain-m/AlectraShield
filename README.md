# AlectraShield

AlectraShield is a Python-based multi-agent deepfake detection orchestrator. It analyzes input media using a four-phase pipeline that extracts assets, performs visual and audio forensic analysis, cross-references contextual provenance, and synthesizes a final deepfake risk verdict.

## Features

- Phase 1: Media ingestion and asset extraction
- Phase 2A: Visual forensic analysis of keyframes
- Phase 2B: Audio biometric analysis of audio streams
- Phase 3: Contextual grounding and provenance verification
- Phase 4: Synthesis of results into a structured detection report

## Repository Structure

- `main.py` — CLI entry point for running the pipeline
- `alectra_shield/orchestrator.py` — async pipeline orchestrator
- `alectra_shield/agents/` — phase-specific agent implementations
- `alectra_shield/models/` — structured output models
- `alectra_shield/utils/` — media extraction and retry helpers
- `tests/` — test suite and test assets

## Requirements

The project uses the following Python packages:

- `google-genai>=1.0.0`
- `opencv-python>=4.9.0`
- `librosa>=0.10.0`
- `scipy>=1.13.0`
- `pydantic>=2.7.0`
- `python-dotenv>=1.0.0`
- `numpy>=1.26.0`

Install them with:

```bash
python -m pip install -r requirements.txt
```

## Environment

Create a `.env` file at the repository root and set the following values:

```env
GOOGLE_API_KEY=your_api_key_here
GEMINI_MODEL="gemini-2.5-flash"
```

`GEMINI_MODEL` controls the Gemini model used by all agents. If unset, the pipeline falls back to `gemini-2.0-flash`.

## Usage

Run the pipeline with a media file:

```bash
python main.py path/to/media.mp4
```

Example output is a JSON-like detection report with:

- `deepfake_detected`
- `confidence_score`
- `analysis_summary`
- `telemetry`

## Architecture

The pipeline follows four phases:

1. **Triage Agent** — extracts audio and visual keyframes from the input media
2. **Visual Forensic Agent** — analyzes image frames for spatial and temporal artifacts
3. **Audio Biometric Agent** — analyzes audio for voice cloning and synthesis signatures
4. **Contextual Agent** — verifies media claims with external grounding
5. **Synthesis Agent** — aggregates telemetry into a final verdict

## Tests

A lightweight test suite is provided in `tests/test_pipeline.py`.

To run the tests:

```bash
python -m pytest tests
```

## Notes

- The current workspace is not initialized as a Git repository, so this README has been created locally.
- To upload to GitHub, initialize the repository with `git init`, add a remote, commit the file, and push it.

```bash
git init
git add README.md
git commit -m "Add project README"
git remote add origin <your-github-repo-url>
git push -u origin main
```
