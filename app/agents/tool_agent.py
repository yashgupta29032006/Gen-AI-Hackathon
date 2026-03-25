from typing import Any, Dict, List
from sqlalchemy.orm import Session
from app.models.models import Task, Event, Note, ExecutionLog
from app.db.session import SessionLocal
from datetime import datetime

class ToolAgent:
    """
    Modular Tool Agent (MCP Style)
    Abstracts direct database and system calls for functional agents.
    """
    def __init__(self):
        self.db = SessionLocal()

    def create_task(self, title: str, description: str = None, due_date: str = None, priority: int = 1) -> Dict[str, Any]:
        due_dt = datetime.fromisoformat(due_date) if due_date else None
        new_task = Task(title=title, description=description, due_date=due_dt, priority=priority)
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return {"id": new_task.id, "status": "created", "title": new_task.title}

    def list_tasks(self) -> List[Dict[str, Any]]:
        tasks = self.db.query(Task).all()
        return [{"id": t.id, "title": t.title, "status": t.status, "due_date": str(t.due_date)} for t in tasks]

    def schedule_event(self, summary: str, start_time: str, end_time: str, description: str = None) -> Dict[str, Any]:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        new_event = Event(summary=summary, start_time=start, end_time=end, description=description)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return {"id": new_event.id, "status": "scheduled", "summary": new_event.summary}

    def save_note(self, content: str, tags: str = None) -> Dict[str, Any]:
        new_note = Note(content=content, tags=tags)
        self.db.add(new_note)
        self.db.commit()
        self.db.refresh(new_note)
        return {"id": new_note.id, "status": "saved"}

    def fetch_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        logs = self.db.query(ExecutionLog).order_by(ExecutionLog.timestamp.desc()).limit(limit).all()
        return [{"agent": l.agent_name, "action": l.action, "details": l.details, "time": str(l.timestamp)} for l in logs]

    def close(self):
        self.db.close()
