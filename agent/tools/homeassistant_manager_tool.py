from langchain_core.tools import tool
from pydantic import BaseModel, Field

from ..core.config import load_config
from ..core.metrics import track_tool
from .http_utils import request_json


class HomeAssistantInput(BaseModel):
    action: str = Field(..., description="list_devices | set_device_state")
    entity_id: str | None = Field(None, description="Target entity ID")
    state: str | None = Field(None, description="New state for set_device_state")


@tool("HomeAssistantManager", args_schema=HomeAssistantInput)
@track_tool
def homeassistant_manager(
    action: str,
    entity_id: str | None = None,
    state: str | None = None,
) -> list | dict | str:
    """Basic tool for Home Assistant operations."""
    cfg = load_config()
    base_url = cfg.homeassistant_url
    token = cfg.homeassistant_token
    if not base_url or not token:
        return "HOMEASSISTANT_URL or HOMEASSISTANT_TOKEN not configured."
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    match action:
        case "list_devices":
            url = f"{base_url}/api/states"
            result = request_json(
                "get",
                url,
                headers=headers,
                status_msg="получаю устройства",
                error_msg="Failed to fetch devices",
            )
            if isinstance(result, list):
                return [item.get("entity_id") for item in result]
            return result
        case "set_device_state":
            if not entity_id or state is None:
                return (
                    "Error: 'entity_id' and 'state' are required for set_device_state"
                )
            url = f"{base_url}/api/states/{entity_id}"
            return request_json(
                "post",
                url,
                headers=headers,
                json={"state": state},
                status_msg="изменяю состояние устройства",
                error_msg="Failed to set device state",
            )
        case _:
            return f"Error: unknown action '{action}'"
