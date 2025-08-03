from langchain_community.llms import FakeListLLM

from agent.agents.researcher_agent import ResearcherAgent


def test_researcher_agent_includes_productivity_tools():
    llm = FakeListLLM(responses=["ok"])
    agent = ResearcherAgent(llm=llm)
    tool_names = {tool.name for tool in agent.tool_list}
    assert "ObsidianManager" in tool_names
    assert "TodoistManager" in tool_names
