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
        try:
            print(f"[Calendar] Creating event with summary: {summary}")
            print(f"[Calendar] Start: {start_time}, End: {end_time}")
            
            # Using Asia/Kolkata as requested by the user
            event_body = {
                'summary': summary,
                'description': description,
                'start': {
                    'dateTime': start_time,
                    'timeZone': 'Asia/Kolkata',
                },
                'end': {
                    'dateTime': end_time,
                    'timeZone': 'Asia/Kolkata',
                },
            }

            print(f"[Calendar] Request Body: {event_body}")
            
            # Execute the real API call
            created_event = self.service.events().insert(
                calendarId='primary', 
                body=event_body
            ).execute()
            
            print(f"[Calendar] Full API Response: {created_event}")
            
            if not created_event.get("id"):
                print("[Calendar] ERROR: No ID returned from Google API!")
                raise Exception("Google API returned success but no event ID.")

            print(f"[Calendar] Event created successfully: {created_event.get('htmlLink')}")
            return {
                "id": created_event.get("id"),
                "html_link": created_event.get("htmlLink"),
                "status": "created_on_google_calendar"
            }
        except Exception as e:
            print(f"[Calendar ERROR]: {str(e)}")
            # Log full details if it's an HttpError
            if hasattr(e, 'content'):
                print(f"[Calendar ERROR Details]: {e.content.decode()}")
            raise e
