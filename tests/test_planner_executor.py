from unittest.mock import patch

from langchain_community.llms import FakeListLLM

from agent.agents.coder_agent import CoderAgent
from agent.agents.planner_executor import PlannerExecutor
from agent.agents.researcher_agent import ResearcherAgent
from agent.agents.router_agent import RouterAgent
from agent.agents.sysops_agent import SysOpsAgent


class TestPlannerExecutor:
    def test_planner_delegates_to_router(self):
        planner_llm = FakeListLLM(responses=['["c","r","s"]', "[]"])

        classifier_llm = FakeListLLM(responses=["coder", "researcher", "sysops"])
        coder_llm = FakeListLLM(responses=["code-res"])
        researcher_llm = FakeListLLM(responses=["research-res"])
        sysops_llm = FakeListLLM(responses=["sysops-res"])

        router = RouterAgent(
            classifier_llm=classifier_llm,
            coder=CoderAgent(llm=coder_llm),
            researcher=ResearcherAgent(llm=researcher_llm),
            sysops=SysOpsAgent(llm=sysops_llm),
        )

        with patch("agent.agents.planner_executor.RouterAgent", return_value=router):
            pe = PlannerExecutor(planner_llm=planner_llm)
            final = pe.run("do stuff")

        assert final == "sysops-res"
