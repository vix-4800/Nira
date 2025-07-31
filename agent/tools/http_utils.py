from typing import Any

import requests

from ..core.status import status_manager


def request_json(
    method: str,
    url: str,
    *,
    status_msg: str,
    error_msg: str,
    timeout: int = 10,
    **kwargs,
) -> Any:
    """Helper for HTTP requests returning JSON.

    Sends a request using ``requests`` with ``status_manager`` feedback and
    handles errors. On success the response JSON is returned; on failure a
    formatted error string is returned.
    """
    try:
        with status_manager.status(status_msg):
            response = getattr(requests, method)(url, timeout=timeout, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except Exception:
            return response.text
    except Exception as exc:
        return f"{error_msg}: {exc}"
