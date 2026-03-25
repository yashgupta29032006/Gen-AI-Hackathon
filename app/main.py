from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.db.session import get_db, engine
from app.db.base import Base
from app.agents.orchestrator import OrchestratorAgent
from app.core.workflow import WorkflowEngine
from app.agents.tool_agent import ToolAgent
import uvicorn

app = FastAPI(title="FlowOS - Multi-Agent Productivity Brain")

# Initialize database
Base.metadata.create_all(bind=engine)

class Query(BaseModel):
    user_input: str

class WorkflowStep(BaseModel):
    agent: str
    action: str
    params: Dict[str, Any]

class ExecutionRequest(BaseModel):
    plan: List[Dict[str, Any]]

@app.post("/ask")
async def ask_orchestrator(query: Query):
    orchestrator = OrchestratorAgent()
    try:
        plan = await orchestrator.execute(query.user_input)
        return plan
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/execute")
async def execute_workflow(request: ExecutionRequest):
    engine = WorkflowEngine()
    orchestrator = OrchestratorAgent()
    
    actions_taken = []
    
    for step in request.plan:
        agent_key = step.get("agent")
        action = step.get("action")
        params = step.get("params", {})
        
        agent = orchestrator.sub_agents.get(agent_key)
        if not agent:
            actions_taken.append({"error": f"Agent {agent_key} not found"})
            continue
            
        try:
            result = await agent.execute(action, params)
            actions_taken.append({
                "agent": agent_key,
                "action": action,
                "result": result
            })
            engine.log_action(agent_key, action, result)
        except Exception as e:
            actions_taken.append({"error": str(e)})

    engine.close()
    return {
        "status": "completed",
        "actions_taken": actions_taken
    }

@app.get("/tasks")
def get_tasks():
    tools = ToolAgent()
    tasks = tools.list_tasks()
    tools.close()
    return tasks

@app.get("/logs")
def get_logs(limit: int = 20):
    tools = ToolAgent()
    logs = tools.fetch_logs(limit=limit)
    tools.close()
    return logs

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
