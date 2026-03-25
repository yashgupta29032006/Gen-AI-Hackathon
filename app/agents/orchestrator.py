from typing import Any, Dict, List
from app.core.agent import BaseAgent
from app.agents.task_agent import TaskAgent
from app.agents.scheduler_agent import SchedulerAgent
from app.agents.notes_agent import NotesAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(name="Orchestrator", role="Parse user intent and delegate to sub-agents.")
        self.sub_agents = {
            "task": TaskAgent(),
            "scheduler": SchedulerAgent(),
            "notes": NotesAgent()
        }

    async def execute(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        1. Parse input to identify goal and plan.
        2. Return a structured plan.
        """
        system_instruction = (
            "You are the Primary Orchestrator for FlowOS. "
            "Your goal is to break down user input into a sequence of executable steps. "
            "Available agents: task, scheduler, notes. "
            "Available actions: "
            "- task: create_task(title, description, due_date, priority), list_tasks() "
            "- scheduler: schedule_event(summary, start_time, end_time, description) "
            "- notes: save_note(content, tags) "
            "\n"
            "Respond with a JSON object containing: "
            "'goal': string summary of user intent, "
            "'plan': list of steps, each step: {'agent': string, 'action': string, 'params': dict}."
        )
        
        plan = await self.get_structured_response(user_input, system_instruction)
        return plan
