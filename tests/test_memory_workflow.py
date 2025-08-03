from unittest.mock import patch
from langchain_community.llms import FakeListLLM

from agent.agents.coder_agent import CoderAgent
from agent.agents.researcher_agent import ResearcherAgent
from agent.agents.sysops_agent import SysOpsAgent
from agent.agents.router_agent import RouterAgent


def _make_agent(db_path):
    classifier_llm = FakeListLLM(responses=["coder"])
    coder_llm = FakeListLLM(responses=["code"])
    researcher_llm = FakeListLLM(responses=["research"])
    sysops_llm = FakeListLLM(responses=["sysops"])
    return RouterAgent(
        classifier_llm=classifier_llm,
        coder=CoderAgent(llm=coder_llm),
        researcher=ResearcherAgent(llm=researcher_llm),
        sysops=SysOpsAgent(llm=sysops_llm),
        memory_db_path=db_path,
    )


def test_remember_and_recall(tmp_path):
    db = tmp_path / "mem.db"
    agent = _make_agent(db)
    resp = agent.ask("remember my favourite colour is blue")
    assert "remembered" in resp.lower()
    result = agent.ask("what is my favourite colour?")
    assert result == "blue"


def test_memory_hit_skips_classification(tmp_path):
    db = tmp_path / "mem.db"
    agent = _make_agent(db)
    agent.ask("remember api key is 123")
    with patch.object(agent, "_classify", wraps=agent._classify) as mock_classify:
        answer = agent.ask("what is api key?")
        assert answer == "123"
        mock_classify.assert_not_called()


def test_memory_miss_uses_classification(tmp_path):
    db = tmp_path / "mem.db"
    agent = _make_agent(db)
    with patch.object(agent, "_classify", wraps=agent._classify) as mock_classify:
        agent.ask("some new task")
        mock_classify.assert_called_once()
