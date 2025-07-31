import unittest

from langchain_community.llms import FakeListLLM

from agent.coder_agent import CoderAgent
from agent.nira_agent import NiraAgent
from agent.researcher_agent import ResearcherAgent
from agent.sysops_agent import SysOpsAgent


class RoutingAgentTest(unittest.TestCase):
    def test_routing_to_specialists(self):
        classifier_llm = FakeListLLM(responses=["coder", "researcher", "sysops"])
        coder_llm = FakeListLLM(responses=["code-result"])
        researcher_llm = FakeListLLM(responses=["research-result"])
        sysops_llm = FakeListLLM(responses=["sysops-result"])

        agent = NiraAgent(
            classifier_llm=classifier_llm,
            coder=CoderAgent(llm=coder_llm),
            researcher=ResearcherAgent(llm=researcher_llm),
            sysops=SysOpsAgent(llm=sysops_llm),
        )

        self.assertEqual(agent.ask("task1"), "code-result")
        self.assertEqual(agent.ask("task2"), "research-result")
        self.assertEqual(agent.ask("task3"), "sysops-result")


if __name__ == "__main__":
    unittest.main()
