import requests
import dns.resolver
from ..env import get_dns_server


def check_website(url: str) -> str:
    """Return HTTP status code for a website or an error message."""
    try:
        resp = requests.head(url, timeout=5)
        return f"{resp.status_code}"
    except Exception as e:
        return f"Error: {e}"


def get_domain_info(domain: str) -> str:
    """Return basic DNS information for a domain."""
    resolver = dns.resolver.Resolver()
    dns_server = get_dns_server()
    if dns_server:
        resolver.nameservers = [dns_server]

    info = []
    try:
        a_records = resolver.resolve(domain, "A")
        info.append("A: " + ", ".join(r.to_text() for r in a_records))
    except Exception:
        info.append("A: ?")
    try:
        mx_records = resolver.resolve(domain, "MX")
        info.append("MX: " + ", ".join(r.exchange.to_text() for r in mx_records))
    except Exception:
        pass
    return "; ".join(info)


__all__ = ["check_website", "get_domain_info"]
