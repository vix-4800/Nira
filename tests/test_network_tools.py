import unittest
from unittest.mock import MagicMock, patch

from agent.tools.check_website_tool import check_website_tool
from agent.tools.get_domain_info_tool import get_domain_info_tool


class NetworkToolsTest(unittest.TestCase):
    @patch("agent.tools.check_website_tool.requests.head")
    def test_check_website(self, mock_head):
        mock_head.return_value.status_code = 200
        result = check_website_tool("https://example.com")
        self.assertEqual(result, "200")
        mock_head.assert_called_once_with("https://example.com", timeout=5)

    @patch("agent.tools.get_domain_info_tool.dns.resolver.Resolver.resolve")
    def test_get_domain_info(self, mock_resolve):
        a_answer = [MagicMock(to_text=lambda: "1.2.3.4")]
        mx_answer = [MagicMock(exchange=MagicMock(to_text=lambda: "mail.example.com."))]
        mock_resolve.side_effect = [a_answer, mx_answer]
        result = get_domain_info_tool("example.com")
        self.assertIn("A: 1.2.3.4", result)
        self.assertIn("MX: mail.example.com.", result)
        self.assertEqual(mock_resolve.call_count, 2)


if __name__ == "__main__":
    unittest.main()
