from fastapi import APIRouter, Request, HTTPException, status, Depends, Query
from fastapi.security import OAuth2AuthorizationCodeBearer
from fastapi.responses import RedirectResponse, JSONResponse
import requests
import os
from dotenv import load_dotenv
from typing import Annotated, List
from app.utils.utils import get_current_user
from app.utils.parsing_tool import extract_plain_text
from app.db.database import db_dependency
from app.models.database_models import User, OutlookAuth, Application, Email
from app.models.pydantic_models import UpdateEmailRequest
from app.utils.email_parser import parse_email_data_hardcoded
from app.routers.application import create_application, update_application
from datetime import datetime, timedelta, timezone
from app.utils.spacy.spacy_parser import parse_email_data_spacy

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

REFRESH_URL = f"https://login.microsoftonline.com/common/oauth2/v2.0/token"

GET_USER = "https://graph.microsoft.com/v1.0/me"

# OAuth2 configuration
SCOPE = "https://graph.microsoft.com/Mail.Read https://graph.microsoft.com/Mail.ReadBasic https://graph.microsoft.com/Calendars.ReadWrite offline_access"
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

# Callback route updates
@router.get("/callback", tags=["Outlook API"])
async def callback(code: str, user: user_dependency, db: db_dependency):
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
    #print(token_json)

    if "access_token" in token_json:
        access_token = {
            "access_token": token_json["access_token"],
            "refresh_token": token_json["refresh_token"],
            "expires_in": token_json["expires_in"],
        }
        
        user_id = user.get("id")
        
        # Calculate the token expiry time
        token_expiry_time = datetime.now(timezone.utc) + timedelta(seconds=access_token["expires_in"])
        
        # Save the access token and refresh token
        create_access_token = OutlookAuth(
            user_id=user_id,
            access_token=access_token["access_token"],
            refresh_token=access_token["refresh_token"],
            token_expiry=token_expiry_time  # Store as a DateTime object
        )
        
        db.add(create_access_token)
        db.commit()
        
        return {"message": "Access token saved", "access_token": access_token}

    return {"error": "Failed to get access token", "response": token_json}

TOKEN_EXPIRATION_TIME = timedelta(hours=1)

def token_is_expired(token_issue_time):
    # Ensure token_issue_time is a DateTime object
    if not isinstance(token_issue_time, datetime):
        raise ValueError("token_issue_time must be a DateTime object")

    # Make current_time offset-aware
    current_time = datetime.now(timezone.utc)

    # Ensure token_issue_time is also offset-aware
    if token_issue_time.tzinfo is None:
        token_issue_time = token_issue_time.replace(tzinfo=timezone.utc)

    return current_time > token_issue_time + TOKEN_EXPIRATION_TIME

async def get_access_token(user_id, db: db_dependency):
    user_id_str = str(user_id)  # Ensure `user_id` is a string
    tokens = db.query(OutlookAuth).filter(OutlookAuth.user_id == user_id_str).first()

    if not tokens:
        # If tokens are missing, prompt re-login
        raise HTTPException(status_code=401, detail="Tokens not found. Please log in.")

    access_token = tokens.access_token
    refresh_token = tokens.refresh_token
    
    # Log the token_expiry for debugging
    #print(f"Token expiry: {tokens.token_expiry}")
    
    # Check if access token exists and is expired
    try:
        if not access_token or token_is_expired(tokens.token_expiry):
            # If access token is expired, refresh it
            new_tokens = await refresh_outlook_token(refresh_token)
            
            if new_tokens:
                # Update the access token and refresh token in the database
                tokens.access_token = new_tokens["access_token"]
                tokens.refresh_token = new_tokens["refresh_token"]
                tokens.token_expiry = new_tokens["expires_in"]
                db.commit()
                access_token = new_tokens["access_token"]
                
            else:
                raise HTTPException(status_code=401, detail="Failed to refresh access token. Please log in again.")
    except ValueError as e:
        # Log the error for debugging
        print(f"Error checking token expiry: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while checking token expiry.")

    return access_token

async def refresh_outlook_token(refresh_token):
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
        # Calculate the new token expiry time
        token_expiry_time = datetime.now(timezone.utc) + timedelta(seconds=token_json["expires_in"])
        
        return {
            "access_token": token_json["access_token"],
            "refresh_token": token_json.get("refresh_token", refresh_token),
            "expires_in": token_expiry_time  # Return as a DateTime object
        }
    else:
        return None

# Secured endpoint requiring valid OAuth2 token
@router.get("/secure-endpoint", tags=["Outlook API"])
async def secure_endpoint(token: str = Depends(oauth2_scheme)):
    return {"message": "You have access to this secure endpoint", "token": token}

# Function to get user's data
@router.get("/get-user", tags=["Outlook API"])
async def get_user(user: user_dependency, db: db_dependency):
    compare_user_id = str(user.get("id"))  # Ensure user_id is a string
    user_id = user.get("id")
    
    # Fetch the access token for the current user
    access_token = await get_access_token(user_id, db)
    
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

    if response.status_code != 200:
        
        # Check if a refresh token is available
        tokens = db.query(OutlookAuth).filter(OutlookAuth.user_id == compare_user_id).first()
        
        if not tokens:
            raise HTTPException(status_code=401, detail="Refresh token not found. Please log in again.")
        
        # Attempt to refresh the access token
        new_tokens = await refresh_outlook_token(tokens.refresh_token)
        
        if new_tokens:
            # Update the access token and refresh token in the database
            tokens.access_token = new_tokens["access_token"]
            tokens.refresh_token = new_tokens["refresh_token"]
            tokens.token_expiry = new_tokens["expires_in"]
            db.commit()
            
            # Retry the request with the new access token
            headers["Authorization"] = f"Bearer {new_tokens['access_token']}"
            response = requests.get(GET_USER, headers=headers)
            outlook_data = response.json()
            
            # Return the updated user data from the Outlook API
            return outlook_data
        else:
            raise HTTPException(status_code=401, detail="Failed to refresh access token. Please log in again.")
        
    
    # Fetch the user from the database
    db_user = db.query(User).filter(User.id == compare_user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found in the database")
    
    # Compare the email from Outlook API and the database, update if necessary
    outlook_email = outlook_data.get('mail')
    if db_user.email != outlook_email:
        db_user.email = outlook_email  # Update the email in the database
        db.commit()
    
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
async def get_user_messages(user: user_dependency, db: db_dependency):
    # Define headers with the access token
    user_id = user.get("id")
    access_token = await get_access_token(user_id, db)
    
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

@router.get("/get-user-messages-by-phrase", tags=["Outlook API"])
async def get_user_messages_by_phrase(
    user: user_dependency,
    db: db_dependency,
    phrases: List[str] = Query(..., description="List of phrases to search for (e.g., 'applying', 'application')"),
): 
    # Define headers with the access token
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Combine multiple phrases into a single search query using OR
    combined_phrases = " OR ".join([f'"{phrase}"' for phrase in phrases])

    # Set the URL with $search query
    url = (
        CURRENT_USER_EMAILS_URL.format(email=email)
        + f"?$search={combined_phrases}&$top=1000"
    )
    
    all_emails = []

    # Loop through pages using @odata.nextLink
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            email_data = response.json()
            all_emails.extend(email_data.get('value', []))
            url = email_data.get('@odata.nextLink')  # Get the next page URL
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching emails.")
    
    # Dictionary to track processed companies
    processed_companies = {}

    # Function to categorize status updates
    def categorize_status(status):
        status = status.lower()
        if any(word in status for word in ["received", "pending", "in progress", "on hold", "reviewed", "candidate"]):
            return "Awaiting Response"
        elif any(word in status for word in ["shortlisted", "accepted", "offer", "hired", "onboarding", "completed", "schedule an interview"]):
            return "Positive Response"
        elif any(word in status for word in ["declined", "rejected", "not been selected", "not selected", "application unsuccessful", "closed", "archived"]):
            return "Rejected"
        else:
            return "Awaiting Response"  # Default to 'Awaiting Response' if no match is found

    all_emails.sort(key=lambda email: email.get('receivedDateTime'))  # Ensure chronological order

    # Iterate through sorted emails to process them
    for email in all_emails:
        email_body = extract_plain_text(email.get('body', {}).get('content', ''))
        email_subject = email.get('subject', "")
        
        if not any(phrase.lower() in email_body.lower() or phrase.lower() in email_subject.lower() for phrase in phrases):
            continue

        body_preview = extract_plain_text(email.get('bodyPreview'))
        entities = parse_email_data_hardcoded(email_body, email_subject)
        parsed_data = parse_email_data_hardcoded(email_body, email_subject)

        company = entities['company']
        applied_date_str = email.get('receivedDateTime')
        applied_date = datetime.fromisoformat(applied_date_str.replace('Z', '+00:00'))
        formatted_applied_date = applied_date.strftime('%m-%d-%Y')
        raw_status = parsed_data['status']
        categorized_status = categorize_status(raw_status)

        interview_date_str = entities.get("interview_date", None)
        interview_date = (
            datetime.fromisoformat(interview_date_str).date()
            if interview_date_str
            else None
        )
        formatted_interview_date = interview_date.strftime('%m-%d-%Y') if interview_date else None

        if company in processed_companies:
            existing_entry = processed_companies[company]

            # Append to previous_emails if the status has changed
            if categorized_status != existing_entry["status"]:
                existing_entry["previous_emails"].append(existing_entry["body"])

            # Append new status to status_history if it's not a duplicate
            if categorized_status not in existing_entry['status_history']:
                existing_entry['status_history'].append(categorized_status)

            # Update details if the email is newer
            if applied_date > existing_entry['applied_date']:
                existing_entry.update({
                    'subject': email_subject,
                    'sender': email.get('from', {}).get('emailAddress', {}).get('address'),
                    'applied_date': applied_date,
                    'formatted_applied_date': formatted_applied_date,
                    'interview_dates': formatted_interview_date,
                    'body_preview': body_preview,
                    'body': email_body,
                    'position': entities['position'],
                    'location': entities.get('location', "Unknown"),
                    'salary': entities.get('salary', "Unknown"),
                    'status': categorized_status
                })
        else:
            # Initialize for a new company
            processed_companies[company] = {
                'subject': email_subject,
                'sender': email.get('from', {}).get('emailAddress', {}).get('address'),
                'applied_date': applied_date,
                'formatted_applied_date': formatted_applied_date,
                'interview_dates': formatted_interview_date,
                'body_preview': body_preview,
                'body': email_body,
                'company': company,
                'position': entities['position'],
                'location': entities.get('location', "Unknown"),
                'salary': entities.get('salary', "Unknown"),
                'status': categorized_status,
                'status_history': [categorized_status],  # Start with the first status
                'previous_emails': []  # Initialize as an empty list
            }

    # Finalizing the payload for the API response
    filtered_emails = [
        {
            'company': company,
            'status_history': data['status_history'],
            'previous_emails': data['previous_emails'],
            'subject': data['subject'],
            'sender': data['sender'],
            'applied_date': data['formatted_applied_date'],
            'interview_dates': data['interview_dates'],
            'body_preview': data['body_preview'],
            'body': data['body'],
            'position': data['position'],
            'location': data['location'],
            'salary': data['salary'],
            'status': data['status']
        }
        for company, data in processed_companies.items()
    ]

    if not filtered_emails:
        return {"message": "No new applications or status updates found"}

    return filtered_emails


# Function to get user's messages filtered by a keyword appearing anywhere in the email and received after the most recent refresh time
@router.get("/get-user-messages-by-phrase-and-date", tags=["Outlook API"])
async def get_user_messages_by_phrase(
    last_refresh_time: str,
    user: user_dependency,
    db: db_dependency,
    phrases: List[str] = Query(..., description="List of phrases to search for (e.g., 'applying', 'application')"),
):
    # Define headers with the access token
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Combine multiple phrases into a single search query using OR
    combined_phrases = " OR ".join([f'"{phrase}"' for phrase in phrases])
    
    # Set the URL with $search query
    url = (
        CURRENT_USER_EMAILS_URL.format(email=email)
        + f"?$search={combined_phrases}&$top=1000"
    )
    
    # Make the request to Microsoft Graph API
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error fetching emails from Microsoft Graph API")
    
    email_data = response.json()
    filtered_emails = []
    user_id_str = str(user_id)

    # Convert last_refresh_time to datetime object
    last_refresh_dt = datetime.fromisoformat(last_refresh_time.replace('Z', '+00:00'))

    # Query the database for existing applications
    applications = db.query(Application).filter(Application.user_id == user_id_str).all()
    processed_companies = {app.company: {} for app in applications}

    def categorize_status(status):
        status = status.lower()
        if any(word in status for word in ["received", "pending", "in progress", "on hold", "reviewed", "candidate"]):
            return "Awaiting Response"
        elif any(word in status for word in ["shortlisted", "accepted", "offer", "hired", "onboarding", "completed", "interview"]):
            return "Positive Response"
        elif any(word in status for word in ["declined", "rejected", "not been selected", "not selected", "application unsuccessful", "closed", "archived"]):
            return "Rejected"
        else:
            return "Awaiting response"  # Default if no match is found

    # Process emails received after the last refresh
    for email in email_data.get('value', []):
        received_time_str = email.get('receivedDateTime')
        received_time = datetime.fromisoformat(received_time_str.replace('Z', '+00:00'))

        if received_time > last_refresh_dt:
            email_body = extract_plain_text(email.get('body', {}).get('content', ''))
            bodyPreview = extract_plain_text(email.get('bodyPreview'))
            entities = parse_email_data_hardcoded(email_body, email.get('subject'))
            parsed_data = parse_email_data_hardcoded(email_body, email.get('subject'))

            company_name = entities.get('company', "Unknown")
            raw_status = parsed_data.get('status', "Unknown")
            categorized_status = categorize_status(raw_status)

            interview_date_str = entities.get("interview_date", None)
            interview_date = (
                datetime.fromisoformat(interview_date_str).date()
                if interview_date_str
                else None
            )  # Parse a single interview date

            if company_name in processed_companies:
                existing_entry = processed_companies[company_name]
                if categorized_status != existing_entry.get("status"):
                    existing_entry["status"] = categorized_status
                if received_time > existing_entry.get("receivedDateTime", received_time):
                    existing_entry["receivedDateTime"] = received_time
                    existing_entry["interview_dates"] = interview_date  # Update single date
            else:
                processed_companies[company_name] = {
                    "subject": email.get("subject"),
                    "from": email.get("from", {}).get("emailAddress", {}).get("address"),
                    "receivedDateTime": received_time,
                    "bodyPreview": bodyPreview,
                    "body": email_body,
                    "company": company_name,
                    "position": entities.get("position", "Unknown"),
                    "location": entities.get("location", "Unknown"),
                    "salary": entities.get("salary", "Unknown"),
                    "status": categorized_status,
                    "interview_dates": interview_date,  # Single date field
                    "status_history": [categorized_status],
                    "previous_emails": {},
                }
                

    filtered_emails = [entry for entry in processed_companies.values() if entry]

    if not filtered_emails:
        return {"message": "No new emails found"}

    return filtered_emails

# Get emails using SpaCy parser
@router.get("/get-user-messages-spacy", tags=["Outlook API"])
async def get_user_messages_spacy(user: user_dependency, db: db_dependency, phrase: str):
    # Define headers with the access token
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)

    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Set initial URL with $top parameter for up to 100 messages
    url = (
        CURRENT_USER_EMAILS_URL.format(email=email)
        + f"?$search=\"{phrase}\"&$top=1000"
    )
    
    all_emails = []

    # Loop through pages using @odata.nextLink
    while url:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            email_data = response.json()
            all_emails.extend(email_data.get('value', []))
            url = email_data.get('@odata.nextLink')  # Get the next page URL
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching emails.")
    
    # Dictionary to track processed companies
    processed_companies = {}

    # Function to categorize status updates
    def categorize_status(status):
        status = status.lower()
        if any(word in status for word in ["received", "pending", "in progress", "on hold", "reviewed", "candidate"]):
            return "Awaiting Response"
        elif any(word in status for word in ["shortlisted", "accepted", "offer", "hired", "onboarding", "completed", "interview"]):
            return "Positive Response"
        elif any(word in status for word in ["declined", "rejected", "not been selected", "not selected", "application unsuccessful", "closed", "archived"]):
            return "Rejected"
        else:
            return "Awaiting Response"  # Default to 'Awaiting Response' if no match is found

    # Process each email
    for email in all_emails:
        email_body = extract_plain_text(email.get('body', {}).get('content', ''))
        bodyPreview = extract_plain_text(email.get('bodyPreview'))
        entities = parse_email_data_spacy(email_body, email.get('subject'))
        parsed_data = parse_email_data_spacy(email_body, email.get('subject'))

        company_name = entities['company']
        received_time = email.get('receivedDateTime')
        raw_status = parsed_data['status']
        categorized_status = categorize_status(raw_status)

        # Check if this company has already been processed
        if company_name in processed_companies:
            existing_entry = processed_companies[company_name]
            
            # Check current state of status phases
            status_history = existing_entry.get('status_history', [])
            
            # Append new status if it's different from the last in `status_history`
            if status_history and categorized_status != status_history[-1]:
                status_history.append(categorized_status)
            
            # Update the most recent status and received time if this email is newer
            if received_time > existing_entry.get('receivedDateTime', received_time):
                existing_entry.update({
                    'subject': email.get('subject'),
                    'from': email.get('from', {}).get('emailAddress', {}).get('address'),
                    'receivedDateTime': received_time,
                    'bodyPreview': bodyPreview,
                    'body': email_body,
                    'position': entities['position'],
                    'location': entities.get('location', "Unknown"),
                    'salary': entities.get('salary', "Unknown"),
                    'status': categorized_status
                })
        else:
            # If it's a new company, add the full email details with initial status in `status_history`
            processed_companies[company_name] = {
                'subject': email.get('subject'),
                'from': email.get('from', {}).get('emailAddress', {}).get('address'),
                'receivedDateTime': received_time,
                'bodyPreview': bodyPreview,
                'body': email_body,
                'company': company_name,
                'position': entities['position'],
                'location': entities.get('location', "Unknown"),
                'salary': entities.get('salary', "Unknown"),
                'status': categorized_status,  # Assign categorized status
                'status_history': [categorized_status],  # Initialize with the first categorized status
                'previous_emails': {}  # Initialize as an empty dictionary
            }

    # Finalize the data for filtered output
    filtered_emails = [
        {
            'company': company,
            'status_history': data['status_history'],
            'subject': data['subject'],
            'from': data['from'],
            'receivedDateTime': data['receivedDateTime'],
            'bodyPreview': data['bodyPreview'],
            'body': data['body'],
            'position': data['position'],
            'location': data['location'],
            'salary': data['salary'],
            'status': data['status']
        }
        for company, data in processed_companies.items()
    ]

    if not filtered_emails:
        return {"message": "No new applications or status updates found"}

    return filtered_emails
        

        
        
    
        
        
























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

# Calendar API

CALENDAR_URL = "https://graph.microsoft.com/v1.0/users/{email}/calendar/events"

@router.post("/create-event", tags=["Outlook API"])
async def create_event(event_data: dict, user: user_dependency, db: db_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(CALENDAR_URL.format(email=email), headers=headers, json=event_data)

    if response.status_code == 201:
        return {"message": "Event created successfully", "event_id": response.json().get("id")}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to create event: {response.text}")
    
@router.put("/update-event", tags=["Outlook API"])
async def update_event(event_id: str, event_data: dict, user: user_dependency, db: db_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.patch(CALENDAR_URL.format(email=email) + f"/{event_id}", headers=headers, json=event_data)

    if response.status_code == 200:
        return {"message": "Event updated successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to update event: {response.text}")
    
@router.delete("/delete-event", tags=["Outlook API"])
async def delete_event(event_id: str, user: user_dependency, db: db_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.delete(CALENDAR_URL.format(email=email) + f"/{event_id}", headers=headers)

    if response.status_code == 204:
        return {"message": "Event deleted successfully"}
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to delete event: {response.text}")
    
@router.get("/get-events", tags=["Outlook API"])
async def get_events(user: user_dependency, db: db_dependency):
    user_id = user.get("id")
    email = user.get("email")
    access_token = await get_access_token(user_id, db)
    
    if not access_token:
        raise HTTPException(status_code=401, detail="Access token not found. Please log in again.")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.get(CALENDAR_URL.format(email=email), headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=f"Failed to retrieve events: {response.text}")
    
