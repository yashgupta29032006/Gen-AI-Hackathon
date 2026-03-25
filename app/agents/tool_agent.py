from typing import Any, Dict, List, Optional
from sqlalchemy.orm import Session
from app.models.models import Task, Event, Note, ExecutionLog
from app.db.session import SessionLocal
from datetime import datetime
from app.services.google_calendar import GoogleCalendarService
from app.utils.oauth import load_token

class ToolAgent:
    """
    Modular Tool Agent (MCP Style)
    Abstracts direct database and system calls for functional agents.
    """
    def __init__(self, user_email: str = "default_user@example.com"):
        self.db = SessionLocal()
        self.user_email = user_email
        self._calendar_service = None

    def _get_calendar_service(self) -> Optional[GoogleCalendarService]:
        if self._calendar_service:
            return self._calendar_service
        
        print(f"[DEBUG] Loading OAuth token for {self.user_email}...")
        creds = load_token(self.db, self.user_email)
        if creds:
            print(f"[DEBUG] Credentials found: {creds.token[:10]}...")
            self._calendar_service = GoogleCalendarService(creds)
            return self._calendar_service
        print("[DEBUG] No credentials found for Google Calendar.")
        return None

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
        print(f"[DEBUG] ToolAgent.schedule_event called for: {summary}")
        google_cal = self._get_calendar_service()
        if google_cal:
            print("[DEBUG] Google Calendar service initialized. Calling create_event...")
            try:
                return google_cal.create_event(summary, start_time, end_time, description)
            except Exception as e:
                print(f"[ToolAgent] Google Calendar creation failed: {str(e)}")
                # Re-raise to ensure the orchestrator/user knows it failed on Google
                raise e
        
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
        new_event = Event(summary=summary, start_time=start, end_time=end, description=description)
        self.db.add(new_event)
        self.db.commit()
        self.db.refresh(new_event)
        return {"id": new_event.id, "status": "scheduled_locally", "summary": new_event.summary}

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
