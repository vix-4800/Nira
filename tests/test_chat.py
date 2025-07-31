import json
import unittest
from pathlib import Path

from langchain_community.llms import FakeListLLM

from agent.base_agent import BaseAgent


class ChatMemoryTest(unittest.TestCase):
    def test_chat_memory_records_messages(self):
        responses = ["hi there", "i am fine"]
        llm = FakeListLLM(responses=responses)
        agent = BaseAgent(llm=llm)
        first = agent.ask("Hello?")
        second = agent.ask("How are you?")
        self.assertEqual(first, "hi there")
        self.assertEqual(second, "i am fine")
        msgs = agent.memory.chat_memory.messages
        self.assertEqual(len(msgs), 4)
        self.assertEqual(msgs[0].content, "Hello?")
        self.assertEqual(msgs[1].content, "hi there")
        self.assertEqual(msgs[2].content, "How are you?")
        self.assertEqual(msgs[3].content, "i am fine")


class ChatLoggingTest(unittest.TestCase):
    def test_chat_logging_records_interactions(self):
        responses = ["hi there", "i am fine"]
        llm = FakeListLLM(responses=responses)
        log_path = Path("chat.log")
        if log_path.exists():
            log_path.unlink()
        agent = BaseAgent(llm=llm, log_file=str(log_path))
        agent.ask("Hello?")
        agent.ask("How are you?")
        lines = log_path.read_text(encoding="utf-8").splitlines()
        self.assertEqual(len(lines), 2)
        first = json.loads(lines[0])
        second = json.loads(lines[1])
        self.assertEqual(first["q"], "Hello?")
        self.assertEqual(first["a"], "hi there")
        self.assertEqual(second["q"], "How are you?")
        self.assertEqual(second["a"], "i am fine")


if __name__ == "__main__":
    unittest.main()
