from unittest.mock import patch

from agent.tools.http_utils import request_json


class TestHttpUtils:
    @patch("agent.tools.http_utils.requests.get")
    def test_request_json_success(self, mock_get):
        mock_get.return_value.raise_for_status.return_value = None
        mock_get.return_value.json.return_value = {"ok": 1}
        result = request_json(
            "get",
            "http://example.com",
            status_msg="getting",
            error_msg="Fail",
        )
        assert result == {"ok": 1}
        mock_get.assert_called_once_with("http://example.com", timeout=10)

    @patch("agent.tools.http_utils.requests.get", side_effect=Exception("boom"))
    def test_request_json_error(self, mock_get):
        result = request_json(
            "get",
            "http://example.com",
            status_msg="getting",
            error_msg="Fail",
        )
        assert "Fail" in result
