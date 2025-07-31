import tempfile

import numpy as np
import sounddevice as sd
from .whisper_utils import transcribe_file


def record_audio(duration: int = 5, samplerate: int = 16000):
    """Record audio from the default microphone."""
    print("🎤 Говорите...")
    audio = sd.rec(
        int(duration * samplerate), samplerate=samplerate, channels=1, dtype="float32"
    )
    sd.wait()
    audio = np.squeeze(audio)
    return audio, samplerate


def transcribe_whisper(duration: int = 5, model_name: str = "base") -> str:
    """Record speech and transcribe it using Whisper."""
    audio, samplerate = record_audio(duration, samplerate=16000)
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        import soundfile as sf

        sf.write(f.name, audio, samplerate)
        text = transcribe_file(f.name, model_name=model_name)
    return text.strip()
