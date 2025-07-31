import dns.resolver
from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..core.config import load_config
from ..core.metrics import track_tool


class DomainInfoInput(BaseModel):
    domain: str = Field(..., description="Domain name")


@tool("GetDomainInfo", args_schema=DomainInfoInput)
@track_tool
def get_domain_info_tool(domain: str) -> str:
    """Get basic DNS information (A and MX records) for a domain."""
    resolver = dns.resolver.Resolver()
    dns_server = load_config().dns_server
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
