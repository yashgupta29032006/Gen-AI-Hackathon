from typing import Any, Dict
from app.core.agent import BaseAgent
from app.agents.tool_agent import ToolAgent

class NotesAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="NotesAgent", role="Capture and retrieve notes and context.")
        self.tools = ToolAgent()

    async def execute(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if action == "save_note":
            return self.tools.save_note(**params)
        else:
            prompt = f"Determine the key points to save for '{action}' with details {params}."
            response = await self.get_structured_response(prompt, "You are a meticulous note-taker.")
            return {"analysis": response}
