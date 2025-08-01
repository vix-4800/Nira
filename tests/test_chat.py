import json
from pathlib import Path

from langchain_community.llms import FakeListLLM

from agent.agents.base_agent import BaseAgent


class TestChatMemory:
    def test_chat_memory_records_messages(self):
        responses = ["hi there", "i am fine"]
        llm = FakeListLLM(responses=responses)
        agent = BaseAgent(llm=llm)
        first = agent.ask("Hello?")
        second = agent.ask("How are you?")
        assert first == "hi there"
        assert second == "i am fine"
        msgs = agent.memory.chat_memory.messages
        assert len(msgs) == 4
        assert msgs[0].content == "Hello?"
        assert msgs[1].content == "hi there"
        assert msgs[2].content == "How are you?"
        assert msgs[3].content == "i am fine"


class TestChatLogging:
    def test_chat_logging_records_interactions(self):
        responses = ["hi there", "i am fine"]
        llm = FakeListLLM(responses=responses)
        log_path = Path("chat.json")
        if log_path.exists():
            log_path.unlink()
        agent = BaseAgent(llm=llm, log_file=str(log_path))
        agent.ask("Hello?")
        agent.ask("How are you?")
        lines = log_path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 2
        first = json.loads(lines[0])
        second = json.loads(lines[1])
        assert first["q"] == "Hello?"
        assert first["a"] == "hi there"
        assert second["q"] == "How are you?"
        assert second["a"] == "i am fine"
