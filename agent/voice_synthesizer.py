import sounddevice
import soundfile
import torch
from TTS.api import TTS

device = "cuda" if torch.cuda.is_available() else "cpu"


class VoiceSynthesizer:
    def __init__(self, model="tts_models/en/ljspeech/tacotron2-DDC") -> None:
        self.tts = TTS(model)

    def speak(self, text: str) -> None:
        self.tts.tts_to_file(text, file_path="output/output.wav", device=device)
        data, sample_rate = soundfile.read("output/output.wav")
        sounddevice.play(data, sample_rate)
        sounddevice.wait()
