from fastapi import APIRouter, Request, HTTPException, status, Depends
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
router = APIRouter()

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
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# OAuth2 configuration
SCOPE = "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.ReadBasic"
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
    return RedirectResponse(url=authorization_url)

# OAuth2 Callback to exchange code for an access token
@router.get("/callback", tags=["Outlook API"])
async def callback(code: str):
    
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
        return {"access_token": access_token}

    return {"error": "Failed to get access token", "response": token_json}

# Secured endpoint requiring valid OAuth2 token
@router.get("/secure-endpoint", tags=["Outlook API"])
async def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "You have access to this secure endpoint", "token": token}


# Function to get user's messages
@router.get("/get-user-messages", tags=["Outlook API"])
async def get_user_messages(email: str, access_token: str):
    # Define headers with the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Construct the full URL with the user's email
    url = CURRENT_USER_EMAILS_URL.format(email=email)
    
    # Make the request to Microsoft Graph API
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve messages: {response.text}")
    

# Function to get user's messages filtered by a keyword appearing anywhere in the email
@router.get("/get-user-messages-by-phrase", tags=["Outlook API"])
async def get_user_messages_by_phrase(email: str, access_token: str, phrase: str):
    # Define headers with the access token
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Construct the full URL with the user's email and $search query to look for the phrase
    url = CURRENT_USER_EMAILS_URL.format(email=email) + f"?$search=\"{phrase}\""

    # Make the request to Microsoft Graph API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        # Parse the response to get only the specific email fields you need (e.g., subject, from, receivedDateTime)
        email_data = response.json()
        filtered_emails = []

        for email in email_data.get('value', []):
            filtered_emails.append({
                'subject': email.get('subject'),
                'from': email.get('from', {}).get('emailAddress', {}).get('address'),
                'receivedDateTime': email.get('receivedDateTime'),
                'bodyPreview': email.get('bodyPreview')
            })

        return filtered_emails
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve messages: {response.text}")

    
