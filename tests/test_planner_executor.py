import unittest

from langchain_community.llms import FakeListLLM

from agent.nira_agent import NiraAgent
from agent.planner_executor import PlannerExecutor


class PlannerExecutorTest(unittest.TestCase):
    def test_planner_executor_sequence(self):
        planner_llm = FakeListLLM(responses=['["one","two"]', "[]"])
        executor_llm = FakeListLLM(responses=["res1", "res2"])
        executor = NiraAgent(llm=executor_llm)
        pe = PlannerExecutor(planner_llm=planner_llm, executor=executor)
        final = pe.run("do stuff")
        self.assertEqual(final, "res2")


if __name__ == "__main__":
    unittest.main()
