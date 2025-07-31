import unittest
from unittest.mock import patch

from agent.tools.proxmox_manager_tool import proxmox_manager
from agent.core.config import load_config


class ProxmoxToolTest(unittest.TestCase):
    def setUp(self):
        load_config.cache_clear()

    @patch("agent.tools.proxmox_manager_tool.request_json")
    def test_list_nodes_success(self, mock_req):
        mock_req.return_value = {"data": [{"node": "pve1"}]}
        env = {
            "PROXMOX_HOST": "https://pve",
            "PROXMOX_TOKEN_ID": "user@pam!id",
            "PROXMOX_TOKEN_SECRET": "secret",
        }
        with patch.dict("os.environ", env):
            result = proxmox_manager.func("list_nodes")
        self.assertEqual(result["data"][0]["node"], "pve1")
        mock_req.assert_called_once()

    @patch("agent.tools.proxmox_manager_tool.request_json")
    def test_missing_node_param(self, mock_req):
        env = {
            "PROXMOX_HOST": "https://pve",
            "PROXMOX_TOKEN_ID": "id",
            "PROXMOX_TOKEN_SECRET": "secret",
        }
        with patch.dict("os.environ", env):
            result = proxmox_manager.func("get_node_stats")
        self.assertIn("'node' is required", result)
        mock_req.assert_not_called()

    def test_missing_config(self):
        with patch.dict("os.environ", {}, clear=True):
            result = proxmox_manager.func("list_nodes")
        self.assertIn("not configured", result)

    @patch("agent.tools.proxmox_manager_tool.request_json")
    def test_filter_running_services(self, mock_req):
        mock_req.return_value = {
            "data": [
                {"name": "sshd", "state": "running"},
                {"name": "pvedaemon", "state": "stopped"},
            ]
        }
        env = {
            "PROXMOX_HOST": "https://pve",
            "PROXMOX_TOKEN_ID": "id",
            "PROXMOX_TOKEN_SECRET": "secret",
        }
        with patch.dict("os.environ", env):
            result = proxmox_manager.func("list_running_services", node="pve1")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["name"], "sshd")
        mock_req.assert_called_once()


if __name__ == "__main__":
    unittest.main()
