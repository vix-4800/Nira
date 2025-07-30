import json
from typing import Any, Dict, List

from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

from .env import get_model, get_server
from .nira_agent import NiraAgent


class PlannerExecutor:
    """Simple planner-executor agent using LangGraph."""

    def __init__(
        self, planner_llm: ChatOllama | None = None, executor: NiraAgent | None = None
    ) -> None:
        model = get_model()
        server = get_server()
        self.planner_llm = planner_llm or ChatOllama(
            model=model, base_url=server, reasoning=False, temperature=0.3
        )
        self.executor = executor or NiraAgent(model_name=model, base_url=server)
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        sg = StateGraph(dict)
        sg.add_node("plan", self._plan_node)
        sg.add_node("execute", self._execute_node)
        sg.set_entry_point("plan")
        sg.add_conditional_edges(
            "plan",
            self._route_from_plan,
            path_map={"execute": "execute", "__end__": END},
        )
        sg.add_conditional_edges(
            "execute",
            self._route_from_execute,
            path_map={"execute": "execute", "__end__": END},
        )
        return sg.compile()

    def _plan(self, goal: str, observation: str) -> List[str]:
        prompt = (
            "You are a planner. "
            "Given the overall goal and last observation, return the next steps as a JSON list.\n"
            f"Goal: {goal}\n"
            f"Observation: {observation}"
        )

        try:
            response = self.planner_llm.predict(prompt)
        except AttributeError:
            raw = self.planner_llm.invoke(prompt)
            response = raw.content if hasattr(raw, "content") else str(raw)

        try:
            steps = json.loads(response)
            if not steps:
                steps = ["(no-plan)"]
            if not isinstance(steps, list):
                steps = [str(steps)]
        except Exception:
            steps = [response.strip()]

        return [str(s) for s in steps]

    def _plan_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        if not state.get("steps") or state["index"] >= len(state["steps"]):
            steps = self._plan(state["goal"], state.get("observation", ""))
            return {
                "goal": state["goal"],
                "steps": steps,
                "index": 0,
                "observation": state.get("observation", ""),
            }
        return state

    def _execute_node(self, state: Dict[str, Any]) -> Dict[str, Any]:
        step = state["steps"][state["index"]]
        result = self.executor.ask(step)
        return {
            "goal": state["goal"],
            "steps": state["steps"],
            "index": state["index"] + 1,
            "observation": result,
        }

    @staticmethod
    def _route_from_plan(state: Dict[str, Any]) -> str:
        return "execute" if state.get("steps") else "__end__"

    @staticmethod
    def _route_from_execute(state: Dict[str, Any]) -> str:
        return "__end__" if state["index"] >= len(state["steps"]) else "execute"

    def run(self, goal: str) -> str:
        state = {"goal": goal, "steps": [], "index": 0, "observation": ""}
        result = self.graph.invoke(state)
        return result.get("observation", "")
