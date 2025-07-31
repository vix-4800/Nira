from langchain_community.llms import FakeListLLM

from agent.agents.base_agent import BaseAgent


class TestAgentConfig:
    def test_default_max_iterations(self):
        llm = FakeListLLM(responses=["hi"])
        agent = BaseAgent(llm=llm)
        assert agent.max_iterations == 15

    def test_custom_max_iterations(self):
        llm = FakeListLLM(responses=["hi"])
        agent = BaseAgent(llm=llm, max_iterations=7)
        assert agent.max_iterations == 7
