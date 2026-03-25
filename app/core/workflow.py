import uuid
from typing import List, Dict, Any
from app.models.models import ExecutionLog
from app.db.session import SessionLocal

class WorkflowEngine:
    def __init__(self):
        self.execution_id = str(uuid.uuid4())
        self.db = SessionLocal()

    def log_action(self, agent_name: str, action: str, details: Dict[str, Any]):
        log_entry = ExecutionLog(
            workflow_id=self.execution_id,
            agent_name=agent_name,
            action=action,
            details=details
        )
        self.db.add(log_entry)
        self.db.commit()

    async def run_chain(self, tasks: List[Dict[str, Any]]):
        """Execute a chain of agent tasks."""
        results = []
        for task in tasks:
            agent = task.get("agent")
            action = task.get("action")
            params = task.get("params", {})
            
            self.log_action(agent.name, f"Starting {action}", params)
            
            try:
                result = await agent.execute(action, params)
                results.append(result)
                self.log_action(agent.name, f"Completed {action}", result)
            except Exception as e:
                error_msg = f"Failed at {action}: {str(e)}"
                self.log_action(agent.name, f"Error at {action}", {"error": error_msg})
                results.append({"error": error_msg})
                break  # Stop chain on failure for now
        
        return results

    def close(self):
        self.db.close()
