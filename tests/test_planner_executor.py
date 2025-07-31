import unittest

from langchain_community.llms import FakeListLLM

from agent.agents.coder_agent import CoderAgent
from agent.agents.nira_agent import NiraAgent
from agent.agents.planner_executor import PlannerExecutor


class PlannerExecutorTest(unittest.TestCase):
    def test_planner_executor_sequence(self):
        planner_llm = FakeListLLM(responses=['["one","two"]', "[]"])
        executor_llm = FakeListLLM(responses=["res1", "res2"])
        classifier_llm = FakeListLLM(responses=["coder", "coder"])
        coder = CoderAgent(llm=executor_llm)
        executor = NiraAgent(classifier_llm=classifier_llm, coder=coder)
        pe = PlannerExecutor(planner_llm=planner_llm, executor=executor)
        final = pe.run("do stuff")
        self.assertEqual(final, "res2")


if __name__ == "__main__":
    unittest.main()
