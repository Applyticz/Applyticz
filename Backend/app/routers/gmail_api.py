import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Request  # FastAPI imports
from fastapi.responses import RedirectResponse
from dotenv import load_dotenv
import requests
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as GoogleRequest  # Google-specific Request

load_dotenv()
router = APIRouter()


# Load environment variables

CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
REDIRECT_URI = "http://localhost:8000/gmail_api/callback"
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# State to keep track of credentials (use a database in production)
token_store = {}


@router.get("/login", tags=["Gmail API"])
async def login():
    print("Here")
    """Initiate the Gmail OAuth login process."""
    print("Registered routes:")
    print(router.routes)

    oauth_url = (
        f"https://accounts.google.com/o/oauth2/auth?"
        f"response_type=code&client_id={CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope={' '.join(SCOPES)}&access_type=offline&prompt=consent"
    )
    return RedirectResponse(url=oauth_url)


@router.get("/callback", tags=["Gmail API"])
async def callback(request: Request):
    """Handle the OAuth callback and exchange the code for an access token."""
    code = request.query_params.get("code")

    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Authorization code not found in callback"
        )

    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    try:
        # Exchange the authorization code for an access token using requests
        token_response = requests.post(token_url, data=token_data)

        print(f"Token response: {token_response.text}") 

        if token_response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch access token: {token_response.text}"
            )

        token_json = token_response.json()
        access_token = token_json.get("access_token")
        refresh_token = token_json.get("refresh_token")

        if not access_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid token response"
            )

        # Save tokens securely (for demonstration purposes, we're saving in-memory)
        token_store["access_token"] = access_token
        token_store["refresh_token"] = refresh_token

        credentials = Credentials(
            token=access_token,
            refresh_token=refresh_token,
            token_uri="https://oauth2.googleapis.com/token",
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET
        )
        service = build('gmail', 'v1', credentials=credentials)
        # if "access_token" in token_json:
        # access_token = {
        #     "access_token": token_json["access_token"],
        #     "refresh_token": token_json["refresh_token"],
        #     "expires_in": token_json["expires_in"],
        # }
        
        # user_id = user.get("id")
        
        # # Calculate the token expiry time
        # token_expiry_time = datetime.now(timezone.utc) + timedelta(seconds=access_token["expires_in"])
        
        # # Save the access token and refresh token
        # create_access_token = OutlookAuth(
        #     user_id=user_id,
        #     access_token=access_token["access_token"],
        #     refresh_token=access_token["refresh_token"],
        #     token_expiry=token_expiry_time  # Store as a DateTime object
        # )
        
        # db.add(create_access_token)
        # db.commit()
        # return {"error": "Failed to get access token", "response": token_json}


        results = service.users().messages().list(userId='me', labelIds=['UNREAD'], maxResults=10).execute()
        messages = results.get('messages', [])

        # Fetch the details of each message
        email_details = []
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            payload = msg.get('payload', {})
            headers = payload.get('headers', [])
            subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
            from_email = next((header['value'] for header in headers if header['name'] == 'From'), 'Unknown Sender')

            email_details.append({
                'id': message['id'],
                'snippet': msg.get('snippet', ''),
                'subject': subject,
                'from': from_email
            })

        # Print and return the email details
        print("Fetched Emails:")
        for email in email_details:
            print(f"From: {email['from']}, Subject: {email['subject']}")

        return {"emails": email_details}
        # return {"access_token": access_token, "refresh_token": refresh_token}

    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while exchanging tokens: {str(e)}"
        )


@router.get("/profile", tags=["Gmail API"])
async def profile():
    """Fetch the Gmail user's profile using the access token."""
    access_token = token_store.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not logged in"
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://www.googleapis.com/gmail/v1/users/me/profile"

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to fetch profile: {response.text}"
            )

        return response.json()

    except requests.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while fetching the profile: {str(e)}"
        )

# @router.get("/messages", tags=["Gmail API"])
# Function to read email message content
def read_message(service, message):
    msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
    payload = msg['payload']
    headers = payload.get("headers")

    if headers:
        for header in headers:
            name = header.get("name")
            value = header.get("value")
            if name.lower() == 'from':
                print("From:", value)
            if name.lower() == "to":
                print("To:", value)
            if name.lower() == "subject":
                print("Subject:", value)
            if name.lower() == "date":
                print("Date:", value)
    print("="*50)

# Function to search messages with a specific query
def search_messages(service, query):
    result = service.users().messages().list(userId='me', q=query).execute()
    messages = result.get('messages', [])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me', q=query, pageToken=page_token).execute()
        messages.extend(result.get('messages', []))
    return messages



# CLIENT_FILE = 'gmailcredentials.json'
# API_NAME = 'gmail'
# API_VERSION = 'v1'
# SCOPES = ['https://mail.google.com/']

# oauth2_sc

# # FastAPI route to handle Google OAuth2 callback
# @router.get('/callback', tags=['gmail_api'])
# async def gmail_api_callback(request: Request):
#     code = request.query_params.get('code')
#     creds = None
    
#     if not code:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Authorization code not found")
    
#     token_url = "https://oauth2.googleapis.com/token"
#     token_data = {
#         'code': code,
#         'client_id': client_id,
#         'client_secret': client_secret,
#         'redirect_uri': redirect_uri,
#         'grant_type': 'authorization_code'
#     }
#     print (client_id +" "+ client_secret +" "+ redirect_uri)
    
#     token_response = requests.post(token_url, data=token_data)
#     token_json = token_response.json()
#     print(token_json)

#     if "access_token" in token_json:
#         access_token = {
#             "access_token": token_json["access_token"],
#             "refresh_token": token_json["refresh_token"],
#             "expires_in": token_json["expires_in"],
#         }

#     # Save token to a JSON file or database here if needed
#     # creds = Credentials(access_token, refresh_token=refresh_token, token_uri=token_url)

#     # Redirect user back to Linked accounts page
#     return RedirectResponse(url="http://localhost:3000/linkedaccounts")

# # Helper function to create Gmail service
# # async def get_accounts(user: None):
# #     return RedirectResponse(url="http://localhost:3000/linkedaccounts")


# # def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
# #     creds = None
# #     working_dir = os.getcwd()
# #     token_dir = 'token files'
# #     token_file = f'token_{api_name}_{api_version}{prefix}.json'
# #     SCOPES = [scope for scope in scopes[0]]

# #     if not os.path.exists(os.path.join(working_dir, token_dir)):
# #         os.mkdir(os.path.join(working_dir, token_dir))

# #     if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
# #         creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)

# #     if not creds or not creds.valid:
# #         if creds and creds.expired and creds.refresh_token:
# #             creds.refresh(GoogleRequest())  # Refresh using Google-specific Request
# #         else:
# #             flow = InstalledAppFlow.from_client_secrets_file(client_secret_file, SCOPES)
# #             creds = flow.run_local_server(port=0)

# #         with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
# #             token.write(creds.to_json())

# #     try:
# #         service = build(api_name, api_version, credentials=creds, static_discovery=False)
# #         print(api_name, api_version, 'service created successfully')
# #         return service
# #     except Exception as e:
# #         print(f'Failed to create service instance for {api_name}: {e}')
# #         return None

# Utility function to convert date to RFC3339 format


# # Main functionality for standalone script
# if __name__ == "__main__":
#     service = create_service(CLIENT_FILE, API_NAME, API_VERSION, SCOPES)
#     if service:
#         service.users().getProfile(userId='me').execute()
#         inp = input("Search Term: ")
#         results = search_messages(service, inp)
#         print(f"Found {len(results)} results.")
#         for msg in results:
#             read_message(service, msg)
