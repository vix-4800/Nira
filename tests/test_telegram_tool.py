import unittest
from unittest.mock import patch

from agent.tools.send_telegram_message_tool import send_telegram_message


class TelegramToolTest(unittest.TestCase):
    @patch("agent.tools.send_telegram_message_tool.requests.post")
    def test_send_message_success(self, mock_post):
        mock_post.return_value.raise_for_status.return_value = None
        with patch.dict(
            "os.environ", {"TELEGRAM_BOT_TOKEN": "token", "TELEGRAM_CHAT_ID": "1"}
        ):
            result = send_telegram_message("hi")
        self.assertEqual(result, "Message sent.")
        mock_post.assert_called_once()

    @patch("agent.tools.send_telegram_message_tool.requests.post")
    def test_missing_env(self, mock_post):
        with patch.dict("os.environ", {}, clear=True):
            result = send_telegram_message("hi")
        self.assertIn("not configured", result)
        mock_post.assert_not_called()

    @patch(
        "agent.tools.send_telegram_message_tool.requests.post",
        side_effect=Exception("fail"),
    )
    def test_send_message_error(self, mock_post):
        with patch.dict(
            "os.environ", {"TELEGRAM_BOT_TOKEN": "token", "TELEGRAM_CHAT_ID": "1"}
        ):
            result = send_telegram_message("hi")
        self.assertIn("Failed to send message", result)


if __name__ == "__main__":
    unittest.main()
