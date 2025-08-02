from __future__ import annotations

from typing import Any

from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.memory import BaseMemory
from langchain_core.messages import get_buffer_string
from pydantic import BaseModel, Field

from .persistent_memory import PersistentMemory


class NiraMemory(BaseMemory, BaseModel):
    """Simple conversation memory without deprecation warnings."""

    chat_memory: InMemoryChatMessageHistory = Field(
        default_factory=InMemoryChatMessageHistory
    )
    persistent_memory: PersistentMemory = Field(default_factory=PersistentMemory)
    memory_key: str = "chat_history"
    persistent_memory_key: str = "persistent_memory"
    input_key: str = "input"
    output_key: str = "output"
    return_messages: bool = False
    human_prefix: str = "Human"
    ai_prefix: str = "AI"

    @property
    def memory_variables(self) -> list[str]:
        return [self.memory_key, self.persistent_memory_key]

    def load_memory_variables(self, inputs: dict[str, Any]) -> dict[str, Any]:
        if self.return_messages:
            buffer: Any = self.chat_memory.messages
        else:
            buffer = get_buffer_string(
                self.chat_memory.messages,
                human_prefix=self.human_prefix,
                ai_prefix=self.ai_prefix,
            )
        return {
            self.memory_key: buffer,
            self.persistent_memory_key: self.persistent_memory.all(),
        }

    def save_context(self, inputs: dict[str, Any], outputs: dict[str, Any]) -> None:
        self.chat_memory.add_user_message(inputs[self.input_key])
        self.chat_memory.add_ai_message(outputs[self.output_key])

    def clear(self) -> None:
        self.chat_memory.clear()
