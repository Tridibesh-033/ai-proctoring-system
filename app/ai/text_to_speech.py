from gtts import gTTS
import uuid
import os

AUDIO_DIR = "static/tts"

os.makedirs(AUDIO_DIR, exist_ok=True)

def generate_tts(text: str) -> str:
    filename = f"{uuid.uuid4()}.mp3"
    filepath = os.path.join(AUDIO_DIR, filename)

    tts = gTTS(text=text, lang="en")
    tts.save(filepath)

    return f"/static/tts/{filename}"
