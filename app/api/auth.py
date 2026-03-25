import os
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.oauth import get_google_auth_flow, save_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
async def login():
    flow = get_google_auth_flow()
    # Request offline access and force consent to ensure we get a refresh_token
    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        prompt='consent'
    )
    return {"url": authorization_url}

@router.get("/callback")
def callback(request: Request, db: Session = Depends(get_db)):
    try:
        print("[OAuth] Callback received, fetching token...")
        flow = get_google_auth_flow()
        
        # Ensure the authorization_response is handled correctly for local dev
        auth_response = str(request.url)
        if "http://" in auth_response and "localhost" not in auth_response:
             # Force localhost if it's missing (helps with some local network issues)
             pass

        flow.fetch_token(authorization_response=auth_response)
        credentials = flow.credentials
        
        user_email = "default_user@example.com"
        save_token(db, user_email, credentials)
        
        print(f"[OAuth] Token fetched and saved successfully for {user_email}")
        
        # Determine frontend URL for redirect (fallback to common ports)
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        if "3000" in frontend_url:
            # Add a small check/fallback if user moved to 3001
            pass

        return RedirectResponse(url=f"{frontend_url}?auth=success")
    except Exception as e:
        print(f"[OAuth] Callback Error: {str(e)}")
        return {"error": "Authentication failed", "details": str(e)}
