from fastapi import APIRouter, Depends, HTTPException, status
from app.utils.utils import get_current_user
from typing import Annotated
from app.db.database import get_db, db_dependency
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse

router = APIRouter()


##NOT SURE WHY THIS ISN'T SHOWING UP ON DOCS 


@router.get('/callback', tags=['gmail_api'])
async def gmail_api_callback(request: Request):
    # Process the authorization code and obtain tokens 

    # Redirect user back to Linked accounts page
    return RedirectResponse(url="http://localhost:3000/linkedaccounts")  # Adjust to your frontend URL


#Make function to handle callback
#Google sends the authorization code here,, so this should process it and return it... THen on frontend, it should recieve it the backend info
#And then it will have the stuff or whatever we want to do


#it recieves the authorization code, then it needs to exchange that for a access token, and will need to refresh periodically
#IMPORTANT:Once you get the access and stuff and authorization token, you need to point back to our main tab