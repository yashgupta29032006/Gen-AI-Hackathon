from typing import Any, Dict
from app.core.agent import BaseAgent
from app.agents.tool_agent import ToolAgent

class SchedulerAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="SchedulerAgent", role="Coordinate calendar events and schedules.")
        self.tools = ToolAgent()

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "schedule_event":
            return self.tools.schedule_event(**params)
        else:
            prompt = f"Suggest a schedule for '{action}' with context {params}."
            response = await self.get_structured_response(prompt, "You are a professional scheduler.")
            return {"suggestion": response}
