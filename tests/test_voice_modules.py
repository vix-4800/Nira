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


if __name__ == "__main__":
    unittest.main()
