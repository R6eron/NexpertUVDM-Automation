# Gemini + Whisper integration for U-V-D-M voice handler
# One-lump Lambo block, 4-space indent – loads .m4a, transcribes, summarizes, hashes, seals

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
import whisper
from google.generativeai import GenerativeModel, configure
from automation.uvdm_safe import UVDM  # import safe UVDM class

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # add to .env
WHISPER_MODEL = "base.en"
VOICE_NOTES_DIR = Path("voice_notes")

configure(api_key=GEMINI_API_KEY)
gemini = GenerativeModel("gemini-1.5-flash")

def lambo_gemini_process():
    audio_files = list(VOICE_NOTES_DIR.glob("*.m4a"))
    if not audio_files:
        return "No new audio found."

    newest_audio = max(audio_files, key=os.path.getctime)
    print(f"Processing: {newest_audio}")

    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(str(newest_audio))
    transcript = result["text"].strip()

    prompt = f"""
    Transcribed voice note:
    {transcript}

    Extract:
    1. Main topic / emotional tone
    2. 1-3 "knowings" (lived truths, scars, insights – short phrases)
    3. Family references (names, sentiment)
    Summarize in 50 words max.
    """
    response = gemini.generate_content(prompt)
    summary = response.text.strip()

    artifact = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": str(newest_audio),
        "transcript": transcript,
        "summary": summary,
        "knowings": [line.strip() for line in summary.split("\n") if line.strip().startswith("-")],
        "hash": hashlib.sha256(transcript.encode()).hexdigest()
    }

    uvdm = UVDM()
    seal_log = uvdm.run()
    print(seal_log)

    artifact_path = Path("immutable_artifacts") / f"artifact_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
    artifact_path.parent.mkdir(exist_ok=True)
    with open(artifact_path, "w") as f:
        json.dump(artifact, f, indent=4)

    return f"Artifact sealed: {artifact_path}\n{seal_log}"

# ────────────────────────────────────────────────
# COMMIT MESSAGE (copy-paste this):
# Add Gemini + Whisper integration for voice transcription, knowings extraction, hashing & UVDM seal
# File: automation/gemini_voice_handler.py
# ────────────────────────────────────────────────