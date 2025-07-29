import os
import sys
import unittest
from pathlib import Path

from langchain_community.llms import FakeListLLM

from agent.nira_agent import NiraAgent

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


class ChatMemoryTest(unittest.TestCase):
    def test_chat_memory_records_messages(self):
        responses = ["hi there", "i am fine"]
        llm = FakeListLLM(responses=responses)
        agent = NiraAgent(llm=llm)
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
        log_path = "chat.log"
        if os.path.exists(log_path):
            os.remove(log_path)
        agent = NiraAgent(llm=llm, log_file=log_path)
        agent.ask("Hello?")
        agent.ask("How are you?")
        with open(log_path, "r") as f:
            lines = f.readlines()
        self.assertEqual(len(lines), 2)
        self.assertIn("Hello?", lines[0])
        self.assertIn("hi there", lines[0])
        self.assertIn("How are you?", lines[1])
        self.assertIn("i am fine", lines[1])


if __name__ == "__main__":
    unittest.main()
