from pathlib import Path

import torch

# Optional dependencies for voice output
try:
    import sounddevice
except Exception:  # pragma: no cover - executed only when missing
    sounddevice = None

try:
    import soundfile
except Exception:  # pragma: no cover - executed only when missing
    soundfile = None

try:
    from TTS.api import TTS
except Exception:  # pragma: no cover - executed only when missing
    TTS = None

device = "cuda" if torch.cuda.is_available() else "cpu"


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

        self.tts = TTS(model)

    def speak(self, text: str):
        if sounddevice is None or soundfile is None:
            raise RuntimeError(
                "sounddevice and soundfile are required for voice playback."
            )

        Path("output").mkdir(exist_ok=True)
        self.tts.tts_to_file(text, file_path="output/output.wav", device=device)
        data, sample_rate = soundfile.read("output/output.wav")
        sounddevice.play(data, sample_rate)
        sounddevice.wait()
