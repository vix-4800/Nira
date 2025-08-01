import json
from typing import Any, Dict, List

from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

from ..core.config import NiraConfig, load_config
from ..core.prompt import load_prompt
from .router_agent import RouterAgent


class PlannerExecutor:
    """Simple planner-executor agent using LangGraph."""

    def __init__(
        self,
        planner_llm: ChatOllama | None = None,
        *,
        config: NiraConfig | None = None,
    ) -> None:
        cfg = config or load_config()
        model = cfg.model
        server = cfg.server
        self.planner_llm = planner_llm or ChatOllama(
            model=model, base_url=server, reasoning=False, temperature=0.3
        )
        self.config = cfg
        self.graph: Any = self._build_graph()

    def _build_graph(self) -> Any:
        sg: Any = StateGraph(dict)
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
        config = load_prompt()
        template = config.get(
            "planner",
            (
                "You are a planner. Given the overall goal and last observation, "
                "return the next steps as a JSON list.\nGoal: {goal}\nObservation: {observation}"
            ),
        )
        prompt = template.replace("{goal}", goal).replace("{observation}", observation)

        try:
            raw = self.planner_llm.invoke(prompt)
            response = raw.content if hasattr(raw, "content") else str(raw)
        except AttributeError:
            response = self.planner_llm.predict(prompt)

        response_str = str(response)
        try:
            steps = json.loads(response_str)
            if not steps:
                steps = ["(no-plan)"]
            if not isinstance(steps, list):
                steps = [str(steps)]
        except Exception:
            steps = [response_str.strip()]

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
        router = RouterAgent(model_name=self.config.model, base_url=self.config.server)
        result = router.ask(step)
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
        result = self.graph.invoke(state)  # type: ignore[attr-defined]
        return result.get("observation", "")
