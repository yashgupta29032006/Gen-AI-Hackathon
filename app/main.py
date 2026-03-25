from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from app.db.session import get_db, engine
from app.db.base import Base
from app.agents.orchestrator import OrchestratorAgent
from app.core.workflow import WorkflowEngine
from app.agents.tool_agent import ToolAgent
from app.api.auth import router as auth_router
import uvicorn
import os
from dotenv import load_dotenv

# Load environment variables explicitly
load_dotenv()

# For local development with HTTP/Google OAuth
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'

app = FastAPI(title="FlowOS - Multi-Agent Productivity Brain")

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:3001", "http://127.0.0.1:3001"],
    allow_origin_regex="http://(localhost|127\.0\.0\.1)(:[0-9]+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    print("[Backend] FlowOS is starting up...")
    required_vars = ["GOOGLE_API_KEY", "GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET"]
    for var in required_vars:
        if not os.getenv(var):
            print(f"[ERROR] Missing required environment variable: {var}")

# Include routers
app.include_router(auth_router)

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
    
    print(f"[EXECUTION] Received request to execute {len(request.plan)} steps.")
    for step in request.plan:
        agent_key = step.get("agent")
        action = step.get("action")
        params = step.get("params", {})
        
        print(f"[EXECUTION] Processing step: {agent_key} -> {action} with params {params}")
        
        agent = orchestrator.sub_agents.get(agent_key)
        if not agent:
            print(f"[EXECUTION] ERROR: Agent {agent_key} not found in orchestrator mapping.")
            actions_taken.append({"error": f"Agent {agent_key} not found"})
            continue
            
        try:
            print(f"[EXECUTION] Calling {agent_key}.execute()...")
            result = await agent.execute(action, params)
            print(f"[EXECUTION] Step completed with result: {result}")
            
            actions_taken.append({
                "agent": agent_key,
                "action": action,
                "result": result
            })
            engine.log_action(agent_key, action, result)
        except Exception as e:
            print(f"[EXECUTION ERROR] Exception during {agent_key}.{action}: {str(e)}")
            actions_taken.append({"error": str(e)})

    engine.close()
    print(f"[EXECUTION] Finished. Returning {len(actions_taken)} results.")
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
