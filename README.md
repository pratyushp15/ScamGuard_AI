# Scam Guard AI

Scam Guard AI classifies message text as `Scam`, `Not Scam`, or `Uncertain` and explains the indicators it found. The Streamlit app also includes a dataset-evaluation view.

## Requirements

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/)
- A Google Gemini API key

## Setup

1. Sync the locked dependencies:

   ```powershell
   uv sync --locked
   ```

2. Create a local `.env` file from the example and set `GEMINI_API_KEY`:

   ```powershell
   Copy-Item .env.example .env
   ```

   Keep `.env` private. It is excluded by `.gitignore`.

3. Start the Streamlit app from the project root:

   ```powershell
   uv run --locked streamlit run streamlit/app.py
   ```

   Open the local URL printed by Streamlit.

## Tests

Run the regression tests without making Gemini API calls:

```powershell
uv run --locked python -m unittest discover -s tests -v
```

## Privacy and API usage

Messages submitted for analysis are sent to Google's Gemini API. Do not submit messages containing information you are not authorized to share. Dataset evaluation makes one API request per message and may incur API usage charges.

## GitHub

This repository contains the source code; GitHub itself does not run the Streamlit app. To host the app, deploy the repository separately to a Streamlit-compatible hosting service and configure `GEMINI_API_KEY` as a deployment secret.
