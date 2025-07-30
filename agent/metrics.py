from __future__ import annotations

import os
from functools import wraps
from prometheus_client import Counter, start_http_server

_METRICS_PORT = int(os.getenv("METRICS_PORT", "8000"))

try:
    start_http_server(_METRICS_PORT)
except Exception:
    pass

# Prometheus counters for tool usage
TOOLS_CALLED_TOTAL = Counter(
    "tools_called_total", "Total number of times a tool was called", ["tool"]
)
TOOL_ERROR_TOTAL = Counter(
    "tool_error_total", "Total number of tool errors", ["tool"]
)


def track_tool(fn):
    """Decorator to track tool usage and errors."""
    tool_name = getattr(fn, "__name__", "unknown")

    @wraps(fn)
    def wrapper(*args, **kwargs):
        TOOLS_CALLED_TOTAL.labels(tool=tool_name).inc()
        try:
            result = fn(*args, **kwargs)
            if isinstance(result, str) and result.lower().startswith("error"):
                TOOL_ERROR_TOTAL.labels(tool=tool_name).inc()
            return result
        except Exception:
            TOOL_ERROR_TOTAL.labels(tool=tool_name).inc()
            raise

    return wrapper

__all__ = ["track_tool", "TOOLS_CALLED_TOTAL", "TOOL_ERROR_TOTAL"]
