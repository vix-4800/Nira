import unittest

from langchain_community.llms import FakeListLLM

from agent.nira_agent import NiraAgent


class AgentConfigTest(unittest.TestCase):
    def test_default_max_iterations(self):
        llm = FakeListLLM(responses=["hi"])
        agent = NiraAgent(llm=llm)
        self.assertEqual(agent.max_iterations, 15)

    def test_custom_max_iterations(self):
        llm = FakeListLLM(responses=["hi"])
        agent = NiraAgent(llm=llm, max_iterations=7)
        self.assertEqual(agent.max_iterations, 7)


if __name__ == "__main__":
    unittest.main()
