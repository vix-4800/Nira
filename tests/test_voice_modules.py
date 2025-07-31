import importlib
import unittest
from unittest.mock import patch


class VoiceModuleDepsTest(unittest.TestCase):
    def test_voice_recognizer_missing_deps(self):
        with patch.dict(
            "sys.modules", {"sounddevice": None, "whisper": None, "soundfile": None}
        ):
            import agent.core.voice_recognizer as vr

            importlib.reload(vr)
            with self.assertRaises(RuntimeError):
                vr.record_audio()
            with self.assertRaises(RuntimeError):
                vr.transcribe_whisper()

    def test_voice_synthesizer_missing_deps(self):
        class FakeCuda:
            @staticmethod
            def is_available():
                return False

        class FakeTorch:
            cuda = FakeCuda()

        with patch.dict(
            "sys.modules",
            {
                "TTS": None,
                "TTS.api": None,
                "sounddevice": None,
                "soundfile": None,
                "torch": FakeTorch(),
            },
        ):
            import agent.core.voice_synthesizer as vs

            importlib.reload(vs)
            with self.assertRaises(RuntimeError):
                vs.VoiceSynthesizer()

    def test_record_audio_status(self):
        import types
        from contextlib import contextmanager

        import numpy as np

        dummy_sd = types.SimpleNamespace()

        def rec(frames, samplerate=16000, channels=1, dtype="float32"):
            return np.zeros((frames, channels), dtype=np.float32)

        dummy_sd.rec = rec
        dummy_sd.wait = lambda: None

        messages = []

        @contextmanager
        def fake_status(msg):
            messages.append(msg)
            yield

        with patch.dict("sys.modules", {"sounddevice": dummy_sd}):
            import agent.core.voice_recognizer as vr

            importlib.reload(vr)
            with patch(
                "agent.core.voice_recognizer.status_manager.status", fake_status
            ):
                audio, sr = vr.record_audio(duration=1, samplerate=16000)

        self.assertEqual(sr, 16000)
        self.assertEqual(audio.shape, (16000,))
        self.assertIn("Говорите", messages[0])

    def test_voice_synthesizer_device_runtime_check(self):
        import types

        class FakeCuda:
            def __init__(self) -> None:
                self._available = False

            def is_available(self):
                return self._available

        fake_cuda = FakeCuda()

        class FakeTorch:
            cuda = fake_cuda

        class DummyTTS:
            def __init__(self, model):
                self.model = model

        dummy_sd = types.SimpleNamespace()
        dummy_sf = types.SimpleNamespace()

        with patch.dict(
            "sys.modules",
            {
                "torch": FakeTorch(),
                "TTS": types.SimpleNamespace(api=types.SimpleNamespace(TTS=DummyTTS)),
                "TTS.api": types.SimpleNamespace(TTS=DummyTTS),
                "sounddevice": dummy_sd,
                "soundfile": dummy_sf,
            },
        ):
            import agent.core.voice_synthesizer as vs

            importlib.reload(vs)
            vs.torch.cuda.is_available = lambda: True
            synth = vs.VoiceSynthesizer()

        self.assertEqual(synth.device, "cuda")


if __name__ == "__main__":
    unittest.main()
