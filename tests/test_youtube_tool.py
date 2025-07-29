import unittest
from unittest.mock import patch

from agent.tools.summarize_youtube_tool import (extract_video_id,
                                                summarize_text,
                                                summarize_youtube_tool)


class YouTubeToolTest(unittest.TestCase):
    def test_extract_video_id(self):
        vid = extract_video_id("https://www.youtube.com/watch?v=abc123xyz12")
        self.assertEqual(vid, "abc123xyz12")

    def test_summarize_text(self):
        summary = summarize_text("One. Two. Three.", sentences=2)
        self.assertEqual(summary, "One. Two.")

    @patch("youtube_transcript_api.YouTubeTranscriptApi.fetch")
    def test_summarize_youtube(self, mock_get):
        mock_get.return_value = [
            {"text": "Hello world."},
            {"text": "Second sentence."},
        ]
        summary = summarize_youtube_tool.func(
            "https://youtu.be/abc123xyz12", sentences=1
        )
        self.assertEqual(summary, "Hello world.")


if __name__ == "__main__":
    unittest.main()
