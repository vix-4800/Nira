from unittest.mock import patch


from agent.core.config import load_config
from agent.tools.telegram_manager_tool import telegram_manager


class TestTelegramTool:
    def setup_method(self):
        load_config.cache_clear()

    @patch("agent.tools.telegram_manager_tool.request_json")
    def test_send_message_success(self, mock_post):
        mock_post.return_value = {}
        with patch.dict(
            "os.environ", {"TELEGRAM_BOT_TOKEN": "token", "TELEGRAM_CHAT_ID": "1"}
        ):
            result = telegram_manager.func("send_message", text="hi")
        assert result == "Message sent."
        mock_post.assert_called_once()

    @patch("agent.tools.telegram_manager_tool.request_json")
    def test_missing_env(self, mock_post):
        with patch.dict("os.environ", {}, clear=True):
            result = telegram_manager.func("send_message", text="hi")
        assert "not configured" in result
        mock_post.assert_not_called()

    @patch(
        "agent.tools.telegram_manager_tool.request_json",
        return_value="Failed to send message: fail",
    )
    def test_send_message_error(self, mock_post):
        with patch.dict(
            "os.environ", {"TELEGRAM_BOT_TOKEN": "token", "TELEGRAM_CHAT_ID": "1"}
        ):
            result = telegram_manager.func("send_message", text="hi")
        assert "Failed to send message" in result
