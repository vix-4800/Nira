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
        data = json.loads(log_path.read_text(encoding="utf-8"))
        assert isinstance(data, list)
        assert len(data) == 2
        first, second = data
        assert first["q"] == "Hello?"
        assert first["a"] == "hi there"
        assert second["q"] == "How are you?"
        assert second["a"] == "i am fine"

    def test_chat_logging_rotates_when_exceeding_limit(self):
        responses = ["first", "second"]
        llm = FakeListLLM(responses=responses)
        # clean up any existing logs
        for p in Path().glob("chat.json*"):
            p.unlink()
        agent = BaseAgent(
            llm=llm,
            log_file="chat.json",
            max_bytes=100,
            backup_count=1,
        )
        agent.ask("Hello?")
        agent.ask("How are you?")
        current = json.loads(Path("chat.json").read_text(encoding="utf-8"))
        backup = json.loads(Path("chat.json.1").read_text(encoding="utf-8"))
        assert len(current) == 1
        assert len(backup) == 1
        assert current[0]["q"] == "How are you?"
        assert backup[0]["q"] == "Hello?"
