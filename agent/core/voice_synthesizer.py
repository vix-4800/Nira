from pathlib import Path
from typing import Any

import torch  # type: ignore[import-not-found]

# Optional dependencies for voice output
try:
    import sounddevice as _sd  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - executed only when missing
    _sd = None
sounddevice: Any | None = _sd

try:
    import soundfile as _sf  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - executed only when missing
    _sf = None
soundfile: Any | None = _sf

try:
    from TTS.api import TTS as _TTS  # type: ignore[import-not-found]
except Exception:  # pragma: no cover - executed only when missing
    _TTS = None
TTS: Any | None = _TTS


class VoiceSynthesizer:
    def __init__(self, model="tts_models/en/ljspeech/tacotron2-DDC") -> None:
        if TTS is None:
            raise RuntimeError(
                "TTS is not installed. Install voice requirements to enable synthesis."
            )
        if sounddevice is None or soundfile is None:
            raise RuntimeError(
                "sounddevice and soundfile are required for voice playback."
            )

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.tts = TTS(model)

    def speak(self, text: str) -> None:
        if sounddevice is None or soundfile is None:
            raise RuntimeError(
                "sounddevice and soundfile are required for voice playback."
            )

        Path("output").mkdir(exist_ok=True)
        self.tts.tts_to_file(text, file_path="output/output.wav", device=self.device)
        data, sample_rate = soundfile.read("output/output.wav")
        sounddevice.play(data, sample_rate)
        sounddevice.wait()
