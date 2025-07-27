class AgentHistory:
    def __init__(self, max_steps=10):
        self.steps = []
        self.max_steps = max_steps

    def add(self, role, content, result=None, status=None):
        step = {
            "role": role,
            "content": content
        }
        if result is not None:
            step["result"] = result
        if status is not None:
            step["status"] = status
        self.steps.append(step)

        if len(self.steps) > self.max_steps:
            self.steps = self.steps[-self.max_steps:]

    def build_prompt(self, task):
        prompt = ""
        for step in self.steps:
            role = step["role"].capitalize()
            prompt += f"{role}: {step['content']}\n"
            if step.get("result"):
                prompt += f"System result: {step['result']}\n"
        prompt += f"User: {task}\nAssistant:"
        return prompt
