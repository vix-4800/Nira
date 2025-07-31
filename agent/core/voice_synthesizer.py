from pathlib import Path

try:  # Optional dependencies for voice output
    import sounddevice
except Exception:  # pragma: no cover - executed only when missing
    sounddevice = None

try:
    import soundfile
except Exception:  # pragma: no cover - executed only when missing
    soundfile = None

import torch

try:
    from TTS.api import TTS
except Exception:  # pragma: no cover - executed only when missing
    TTS = None


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

    def speak(self, text: str):
        if sounddevice is None or soundfile is None:
            raise RuntimeError(
                "sounddevice and soundfile are required for voice playback."
            )

        Path("output").mkdir(exist_ok=True)
        self.tts.tts_to_file(text, file_path="output/output.wav", device=self.device)
        data, sample_rate = soundfile.read("output/output.wav")
        sounddevice.play(data, sample_rate)
        sounddevice.wait()
