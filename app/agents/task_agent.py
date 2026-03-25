from typing import Any, Dict
from app.core.agent import BaseAgent
from app.agents.tool_agent import ToolAgent

class TaskAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="TaskAgent", role="Manage user tasks and to-do lists.")
        self.tools = ToolAgent()

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "create_task":
            return self.tools.create_task(**params)
        elif action == "list_tasks":
            return {"tasks": self.tools.list_tasks()}
        else:
            # LLM reasoning for ambiguous commands
            prompt = f"Explain how to perform '{action}' with params {params} for task management."
            response = await self.get_structured_response(prompt, "You are a task management expert.")
            return {"reasoning": response}
