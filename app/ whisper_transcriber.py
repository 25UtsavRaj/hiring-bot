# app/whisper_transcriber.py

import whisper
import os

# Load whisper model once
model = whisper.load_model("base")  # You can use 'small' or 'medium' for better accuracy

def transcribe_audio(file_path: str) -> str:
    """
    Transcribes the audio file to text using OpenAI's Whisper.
    """
    try:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Audio file not found: {file_path}")

        result = model.transcribe(file_path)
        return result.get("text", "").strip()
    except Exception as e:
        print(f"Transcription failed: {e}")
        return ""
