import json
from pathlib import Path

class ConfigError(Exception):
    """Raised when there is an issue loading the prompt configuration."""


def load_prompt(path: str | Path = Path("prompt.json")) -> dict:
    """Load the prompt configuration from ``path``.

    Parameters
    ----------
    path: str | Path
        Path to the JSON configuration file. Defaults to ``prompt.json`` in the
        current working directory.

    Returns
    -------
    dict
        Parsed JSON configuration.

    Raises
    ------
    ConfigError
        If the file does not exist or contains invalid JSON.
    """
    path = Path(path)
    try:
        with path.open("r", encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError as exc:
        raise ConfigError(f"{path} not found") from exc
    except json.JSONDecodeError as exc:
        raise ConfigError(f"{path} is not valid JSON") from exc

