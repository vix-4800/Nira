import unittest
from unittest.mock import patch

from agent.tools.homeassistant_manager_tool import homeassistant_manager
from agent.core.config import load_config


class HomeAssistantToolTest(unittest.TestCase):
    def setUp(self):
        load_config.cache_clear()

    @patch("agent.tools.homeassistant_manager_tool.request_json")
    def test_list_devices(self, mock_request):
        mock_request.return_value = [
            {"entity_id": "light.kitchen"},
            {"entity_id": "sensor.temp"},
        ]
        with patch.dict(
            "os.environ",
            {"HOMEASSISTANT_URL": "http://ha", "HOMEASSISTANT_TOKEN": "tok"},
        ):
            result = homeassistant_manager.func("list_devices")
        self.assertEqual(result, ["light.kitchen", "sensor.temp"])
        mock_request.assert_called_once()

    @patch("agent.tools.homeassistant_manager_tool.request_json")
    def test_set_device_state(self, mock_request):
        mock_request.return_value = {"entity_id": "light.kitchen", "state": "on"}
        with patch.dict(
            "os.environ",
            {"HOMEASSISTANT_URL": "http://ha", "HOMEASSISTANT_TOKEN": "tok"},
        ):
            result = homeassistant_manager.func(
                "set_device_state", entity_id="light.kitchen", state="on"
            )
        self.assertEqual(result, {"entity_id": "light.kitchen", "state": "on"})
        mock_request.assert_called_once()

    @patch("agent.tools.homeassistant_manager_tool.request_json")
    def test_missing_env(self, mock_request):
        with patch.dict("os.environ", {}, clear=True):
            result = homeassistant_manager.func("list_devices")
        self.assertIn("not configured", result)
        mock_request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
