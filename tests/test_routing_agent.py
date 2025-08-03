from unittest.mock import patch

from langchain_community.llms import FakeListLLM

from agent.agents.coder_agent import CoderAgent
from agent.agents.researcher_agent import ResearcherAgent
from agent.agents.router_agent import RouterAgent
from agent.agents.sysops_agent import SysOpsAgent


class TestRoutingAgent:
    def test_routing_to_specialists(self, tmp_path):
        classifier_llm = FakeListLLM(responses=["coder", "researcher", "sysops"])
        memory_llm = FakeListLLM(responses=["none", "none", "none"])
        coder_llm = FakeListLLM(responses=["code-result"])
        researcher_llm = FakeListLLM(responses=["research-result"])
        sysops_llm = FakeListLLM(responses=["sysops-result"])

        agent = RouterAgent(
            classifier_llm=classifier_llm,
            memory_llm=memory_llm,
            coder=CoderAgent(llm=coder_llm),
            researcher=ResearcherAgent(llm=researcher_llm),
            sysops=SysOpsAgent(llm=sysops_llm),
            memory_db_path=tmp_path / "mem.db",
        )

        assert agent.ask("task1") == "code-result"
        assert agent.ask("task2") == "research-result"
        assert agent.ask("task3") == "sysops-result"

    def test_load_prompt_only_called_on_init(self, tmp_path):
        with patch("agent.agents.router_agent.load_prompt") as mock_load:
            mock_load.return_value = {"classify": "label {task}"}
            classifier_llm = FakeListLLM(responses=["coder", "researcher"])
            memory_llm = FakeListLLM(responses=["none", "none"])
            coder_llm = FakeListLLM(responses=["c1", "c2"])
            researcher_llm = FakeListLLM(responses=["r1"])
            sysops_llm = FakeListLLM(responses=["s1"])

            agent = RouterAgent(
                classifier_llm=classifier_llm,
                memory_llm=memory_llm,
                coder=CoderAgent(llm=coder_llm),
                researcher=ResearcherAgent(llm=researcher_llm),
                sysops=SysOpsAgent(llm=sysops_llm),
                memory_db_path=tmp_path / "mem.db",
            )

            agent.ask("one")
            agent.ask("two")

            assert mock_load.call_count == 1
