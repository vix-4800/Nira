import tempfile
from typing import Any

import numpy as np

from .status import status_manager
from .whisper_utils import transcribe_file

sd: Any | None = None

try:  # Optional dependency
    import sounddevice as _sd  # type: ignore[import-not-found]

    sd = _sd
except Exception:  # pragma: no cover - executed only when missing
    pass


def record_audio(duration: int = 5, samplerate: int = 16000):
    """Record audio from the default microphone."""
    if sd is None:
        raise RuntimeError(
            "sounddevice is not installed. Install voice requirements to enable recording."
        )

    with status_manager.status("🎤 Говорите..."):
        audio = sd.rec(
            int(duration * samplerate),
            samplerate=samplerate,
            channels=1,
            dtype="float32",
        )
        sd.wait()
    audio = np.squeeze(audio)
    return audio, samplerate


def transcribe_whisper(duration: int = 5, model_name: str = "base") -> str:
    """Record speech and transcribe it using Whisper."""
    audio, samplerate = record_audio(duration, samplerate=16000)
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        try:  # Optional dependency
            import soundfile as sf  # type: ignore[import-not-found]
        except Exception as exc:
            raise RuntimeError(
                "soundfile is not installed. Install voice requirements to enable recognition."
            ) from exc

        sf.write(f.name, audio, samplerate)
        text = transcribe_file(f.name, model_name=model_name)
    return text.strip()
