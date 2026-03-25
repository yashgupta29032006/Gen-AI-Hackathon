from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.utils.oauth import get_google_auth_flow, save_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/login")
def login():
    flow = get_google_auth_flow()
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    return {"url": authorization_url}

@router.get("/callback")
def callback(request: Request, db: Session = Depends(get_db)):
    flow = get_google_auth_flow()
    flow.fetch_token(authorization_response=str(request.url))
    credentials = flow.credentials
    
    # In a real app, you'd get the user email from the token or session
    # For this demo, we'll use a default email
    user_email = "default_user@example.com"
    save_token(db, user_email, credentials)
    
    return RedirectResponse(url="http://localhost:3000?auth=success")
