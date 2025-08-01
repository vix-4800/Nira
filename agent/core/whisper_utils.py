import importlib
from typing import Any, Dict

whisper: Any | None = None
_models: Dict[str, Any] = {}


def _load_whisper() -> Any:
    global whisper
    if whisper is None:
        try:
            whisper = importlib.import_module("whisper")
        except Exception as exc:
            raise RuntimeError("whisper package not installed") from exc
    return whisper


def get_model(model_name: str = "base") -> Any:
    module = _load_whisper()
    model = _models.get(model_name)
    if model is None:
        model = module.load_model(model_name)
        _models[model_name] = model
    return model


def transcribe_file(path: str, model_name: str = "base") -> str:
    model = get_model(model_name)
    result = model.transcribe(path)
    return result.get("text", "").strip()
