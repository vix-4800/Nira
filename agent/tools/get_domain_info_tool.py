from pydantic import BaseModel, Field
from langchain_core.tools import tool

from .network_tools import get_domain_info

class DomainInfoInput(BaseModel):
    domain: str = Field(..., description="Domain name")

@tool("GetDomainInfo", args_schema=DomainInfoInput)
def get_domain_info_tool(domain: str) -> str:
    """Get basic DNS information (A and MX records) for a domain."""
    return get_domain_info(domain)
