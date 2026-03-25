from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from typing import Dict, Any, Optional
from datetime import datetime

class GoogleCalendarService:
    def __init__(self, credentials: Credentials):
        self.service = build("calendar", "v3", credentials=credentials)

    def create_event(self, summary: str, start_time: str, end_time: str, description: str = None) -> Dict[str, Any]:
        """
        Creates a real Google Calendar event.
        Expects ISO format strings for start_time and end_time.
        """
        event = {
            'summary': summary,
            'description': description,
            'start': {
                'dateTime': start_time,
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time,
                'timeZone': 'UTC',
            },
        }

        created_event = self.service.events().insert(calendarId='primary', body=event).execute()
        return {
            "id": created_event.get("id"),
            "html_link": created_event.get("htmlLink"),
            "status": "created_on_google_calendar"
        }
