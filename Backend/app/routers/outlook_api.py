from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv
from typing import Annotated
from app.utils.utils import get_current_user
from app.utils.parsing_tool import extract_plain_text
from app.db.database import db_dependency
from app.models.database_models import User, Application
from app.models.pydantic_models import UpdateEmailRequest
from app.utils.email_parser import extract_company_and_position, parse_email_data_hardcoded
from app.routers.application import create_application, update_application
from datetime import datetime


# Load environment variables from .env file
load_dotenv()
router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


# MSAL configuration from environment variables
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
TENANT_ID = os.getenv('TENANT_ID')
REDIRECT_URL = os.getenv('REDIRECT_URL')

# Ensure all environment variables are set
if not CLIENT_ID or not CLIENT_SECRET or not TENANT_ID or not REDIRECT_URL:
    raise Exception("Environment variables CLIENT_ID, CLIENT_SECRET, TENANT_ID, or REDIRECT_URI are missing.")

# MSAL URLs
AUTH_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/authorize"
TOKEN_URL = "https://login.microsoftonline.com/common/oauth2/v2.0/token"
CURRENT_USER_EMAILS_URL = "https://graph.microsoft.com/v1.0/me/messages"
USER_EMAILS_URL = "https://graph.microsoft.com/v1.0/users/{email}/messages"
USER_BY_EMAIL_URL = "https://graph.microsoft.com/v1.0/users/{email}"
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

GET_USER = "https://graph.microsoft.com/v1.0/me"

# OAuth2 configuration
SCOPE = "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.ReadBasic https://graph.microsoft.com/Calendars.ReadWrite"
STATE = "12345"

# OAuth2 Authorization Code Bearer
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTH_URL,
    tokenUrl=TOKEN_URL
)

# Route to trigger OAuth login flow
@router.get("/login", tags=["Outlook API"])
async def login():
    authorization_url = (
        f"{AUTH_URL}?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URL}"
        f"&scope={SCOPE.replace(' ', '%20')}"
    )
    print(authorization_url)
    return RedirectResponse(url=authorization_url)

# Simple in-memory storage for access tokens (use a proper store in production)
user_tokens = {}

@router.get("/callback", tags=["Outlook API"])
async def callback(code: str, user: user_dependency):
    
    # Exchange the authorization code for an access token
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URL,
        "scope": SCOPE
    }

    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    if "access_token" in token_json:
        access_token = token_json["access_token"]
        
        # Save the access token associated with a user from user dependency
        user_id = user.get("id")
        user_tokens[user_id] = access_token
        
        return {"message": "Access token saved", "access_token": access_token}

    return {"error": "Failed to get access token", "response": token_json}

# Secured endpoint requiring valid OAuth2 token
@router.get("/secure-endpoint", tags=["Outlook API"])
async def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "You have access to this secure endpoint", "token": token}

# Function to get user's data
@router.get("/get-user", tags=["Outlook API"])
async def get_user(user: user_dependency, db: db_dependency):
    compare_user_id = str(user.get("id"))  # Ensure user_id is a string
    user_id = user.get("id")
    print("User ID:", user_id)
    
    # Fetch the access token for the current user
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    # Prepare the request headers
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Make a request to the Outlook API to get the user information
    response = requests.get(GET_USER, headers=headers)
    outlook_data = response.json()
    print(outlook_data)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve user data: {response.text}")
    
    # Fetch the user from the database
    db_user = db.query(User).filter(User.id == compare_user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found in the database")
    
    # Compare the email from Outlook API and the database, update if necessary
    outlook_email = outlook_data.get('mail')
    if db_user.email != outlook_email:
        db_user.email = outlook_email  # Update the email in the database
        db.commit()
        print(f"Email updated to {outlook_email}")
    
    # Return the updated user data from the Outlook API
    return outlook_data

@router.post("/update-email", tags=["Users"])
async def update_email(user: user_dependency, db: db_dependency, email_request: UpdateEmailRequest):
    user_id = str(user.get("id"))  # Get the user ID from the dependency
    new_email = email_request.new_email

    # Fetch the user from the database
    db_user = db.query(User).filter(User.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found in the database")
    
    # Update the email and commit the changes
    db_user.email = new_email
    db.commit()
    
    return {"message": "Email updated successfully", "new_email": new_email}



@router.get("/get-user-messages", tags=["Outlook API"])
async def get_user_messages(user: user_dependency):
    # Define headers with the access token
    user_id = user.get("id")
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Make the request to Microsoft Graph API
    response = requests.get(CURRENT_USER_EMAILS_URL, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve messages: {response.text}")
    

# Function to get user's messages filtered by a keyword appearing anywhere in the email
@router.get("/get-user-messages-by-phrase", tags=["Outlook API"])
async def get_user_messages_by_phrase(phrase: str, last_refresh_time: str, user: user_dependency, db: db_dependency):
    # Define headers with the access token
    user_id = user.get("id")
    email = user.get("email")
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Construct the full URL with the user's email and $search query to look for the phrase
    url = CURRENT_USER_EMAILS_URL.format(email=email) + f"?$search=\"{phrase}\""

    # Make the request to Microsoft Graph API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        email_data = response.json()
        filtered_emails = []

        # Convert last_refresh_time to datetime object
        last_refresh_dt = datetime.fromisoformat(last_refresh_time.replace('Z', '+00:00'))

        # Filter emails by receivedDateTime based on last_refresh_time
        for email in email_data.get('value', []):
            received_time_str = email.get('receivedDateTime')
            received_time = datetime.fromisoformat(received_time_str.replace('Z', '+00:00'))

            # Only add emails received after the last refresh time
            if received_time > last_refresh_dt:
                filtered_emails.append({
                    'subject': email.get('subject'),
                    'from': email.get('from', {}).get('emailAddress', {}).get('address'),
                    'receivedDateTime': received_time_str,
                    'bodyPreview': extract_plain_text(email.get('bodyPreview')),
                    'body': extract_plain_text(email.get('body', {}).get('content', ''))
                })
            else:
                print(f"Skipping email received at {received_time} as it is older than {last_refresh_dt}")
        
        # Sort emails by 'receivedDateTime' (oldest first)
        filtered_emails.sort(key=lambda x: x['receivedDateTime'])

        # If no new emails are found, return an empty list and the refresh time
        if not filtered_emails:
            return JSONResponse(content={"emails": [], "last_refresh_time": last_refresh_time})
        
        # Return the filtered emails with the last refresh time
        return JSONResponse(content={"emails": filtered_emails, "last_refresh_time": last_refresh_time})

    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve messages: {response.text}")

    
# Function to get a refresh token for Outlook API
@router.get("/refresh-token", tags=["Outlook API"], status_code=status.HTTP_200_OK)
async def refresh_token(refresh_token: str):
    token_data = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "scope": SCOPE
    }

    token_response = requests.post(TOKEN_URL, data=token_data)
    token_json = token_response.json()

    if "access_token" in token_json:
        access_token = token_json["access_token"]
        return {"message": "Access token refreshed", "access_token": access_token}

    return {"error": "Failed to refresh access token", "response": token_json}

# Calander API

CALANDER_URL = "https://graph.microsoft.com/v1.0/users/{email}/calendar/events"

@router.post("/create-event", tags=["Outlook API"])
async def create_event(event_data: dict, user: user_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(CALANDER_URL.format(email=email), headers=headers, json=event_data)

    if response.status_code == 201:
        return {"message": "Event created successfully", "event_id": response.json().get("id")}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to create event: {response.text}")
    
@router.put("/update-event", tags=["Outlook API"])
async def update_event(event_id: str, event_data: dict, user: user_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(CALANDER_URL.format(email=email) + f"/{event_id}", headers=headers, json=event_data)

    if response.status_code == 200:
        return {"message": "Event updated successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to update event: {response.text}")
    
@router.delete("/delete-event", tags=["Outlook API"])
async def delete_event(event_id: str, user: user_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.delete(CALANDER_URL.format(email=email) + f"/{event_id}", headers=headers)

    if response.status_code == 204:
        return {"message": "Event deleted successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to delete event: {response.text}")
    
@router.get("/get-events", tags=["Outlook API"])
async def get_events(user: user_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = user_tokens.get(user_id)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(CALANDER_URL.format(email=email), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve events: {response.text}")
    
