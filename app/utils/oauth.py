import os
import json
from base64 import b64encode, b64decode
from typing import Optional
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from sqlalchemy.orm import Session
from app.models.models import OAuthToken
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
REDIRECT_URI = os.getenv("REDIRECT_URI", "http://localhost:8000/auth/callback")

SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Static verifier to bypass standard PKCE state issues in a stateless FastAPI backend
# This ensures the verifier generated during login matches the one expected in the callback.
STATIC_VERIFIER = "flowos_stateless_verifier_2024_productivity_brain_secure_random_string"

def get_google_auth_flow() -> Flow:
    print("[OAuth] Creating Google Auth Flow...")
    client_config = {
        "web": {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = Flow.from_client_config(
        client_config,
        scopes=SCOPES,
        redirect_uri=REDIRECT_URI
    )
    # Set a fixed verifier to disable dynamic PKCE generation/loss
    flow.code_verifier = STATIC_VERIFIER
    return flow

def save_token(db: Session, user_email: str, credentials: Credentials):
    print(f"[OAuth] Saving token for {user_email}...")
    token_data = credentials.to_json()
    db_token = db.query(OAuthToken).filter(OAuthToken.user_email == user_email).first()
    if not db_token:
        db_token = OAuthToken(user_email=user_email, token=token_data)
        db.add(db_token)
    else:
        db_token.token = token_data
    
    db_token.refresh_token = credentials.refresh_token
    db_token.token_uri = credentials.token_uri
    db_token.client_id = credentials.client_id
    db_token.client_secret = credentials.client_secret
    db_token.scopes = ",".join(credentials.scopes)
    
    db.commit()
    print(f"[OAuth] Token saved to database.")

def load_token(db: Session, user_email: str) -> Optional[Credentials]:
    print(f"[OAuth] Loading token for {user_email}...")
    db_token = db.query(OAuthToken).filter(OAuthToken.user_email == user_email).first()
    if not db_token:
        print(f"[OAuth] No token found in DB for {user_email}")
        return None
    
    creds = Credentials.from_authorized_user_info(json.loads(db_token.token), SCOPES)
    if creds and creds.expired and creds.refresh_token:
        print(f"[OAuth] Token expired, attempting refresh...")
        try:
            creds.refresh(Request())
            save_token(db, user_email, creds)
            print(f"[OAuth] Token refreshed successfully.")
        except Exception as e:
            print(f"[OAuth] Refresh error: {str(e)}")
            return None
    
    return creds
