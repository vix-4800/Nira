from unittest.mock import MagicMock, patch

from agent.tools.get_domain_info_tool import get_domain_info_tool


class TestNetworkTools:
    @patch("agent.tools.get_domain_info_tool.dns.resolver.Resolver.resolve")
    def test_get_domain_info(self, mock_resolve):
        a_answer = [MagicMock(to_text=lambda: "1.2.3.4")]
        mx_answer = [MagicMock(exchange=MagicMock(to_text=lambda: "mail.example.com."))]
        mock_resolve.side_effect = [a_answer, mx_answer]
        result = get_domain_info_tool.func("example.com")
        assert "A: 1.2.3.4" in result
        assert "MX: mail.example.com." in result
        assert mock_resolve.call_count == 2
