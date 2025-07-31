from typing import Any, List

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..core.config import load_config
from ..core.metrics import track_tool
from .http_utils import request_json


class ProxmoxManagerInput(BaseModel):
    action: str = Field(
        ..., description="list_nodes | get_node_stats | list_running_services"
    )
    node: str | None = Field(None, description="Target node for node-specific actions")


@tool("ProxmoxManager", args_schema=ProxmoxManagerInput)
@track_tool
def proxmox_manager(action: str, node: str | None = None) -> Any:
    """Unified tool for basic Proxmox operations."""
    cfg = load_config()
    host = cfg.proxmox_host
    token_id = cfg.proxmox_token_id
    token_secret = cfg.proxmox_token_secret
    verify = cfg.proxmox_verify_ssl

    if not host or not token_id or not token_secret:
        return "PROXMOX credentials not configured."

    base = host.rstrip("/")
    headers = {"Authorization": f"PVEAPIToken={token_id}={token_secret}"}

    match action:
        case "list_nodes":
            url = f"{base}/api2/json/nodes"
            return request_json(
                "get",
                url,
                headers=headers,
                verify=verify,
                status_msg="получаю список узлов",
                error_msg="Failed to list nodes",
            )
        case "get_node_stats":
            if not node:
                return "Error: 'node' is required for get_node_stats"
            url = f"{base}/api2/json/nodes/{node}/status"
            return request_json(
                "get",
                url,
                headers=headers,
                verify=verify,
                status_msg="получаю статистику узла",
                error_msg="Failed to get node stats",
            )
        case "list_running_services":
            if not node:
                return "Error: 'node' is required for list_running_services"
            url = f"{base}/api2/json/nodes/{node}/services"
            result = request_json(
                "get",
                url,
                headers=headers,
                verify=verify,
                status_msg="получаю сервисы",
                error_msg="Failed to list services",
            )
            if isinstance(result, str):
                return result
            if isinstance(result, dict) and isinstance(result.get("data"), list):
                running: List[dict] = [
                    srv for srv in result["data"] if srv.get("state") == "running"
                ]
                return running
            return result
        case _:
            return f"Error: unknown action '{action}'"
