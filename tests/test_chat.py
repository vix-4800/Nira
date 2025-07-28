import unittest
from agent.nira_agent import NiraAgent
from langchain_community.llms import FakeListLLM

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

if __name__ == '__main__':
    unittest.main()
