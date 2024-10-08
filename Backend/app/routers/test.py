from fastapi import APIRouter, HTTPException, status, Depends, Body, Header
from app.db.database import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder
from app.models.database_models import Test, User
from app.models.pydantic_models import TestBase, GreetResponse
from app.db.database import db_dependency
from fastapi.responses import HTMLResponse

router = APIRouter()

@router.get('/testing_route', tags=['test'])
async def test():
  return {'message': 'Testing Route'}

@router.get("/test-db", tags=["test"])
def test_db_connection(db: Session = Depends(get_db)):
    try:
        # Fetch the first user from the 'users' table
        user = db.query(User).first()

        if user:
            # Convert the SQLAlchemy model to a dictionary
            user_data = jsonable_encoder(user)
            return {"status": "Database connected successfully!", "user": user_data}
        else:
            return {"status": "Database connected successfully!", "message": "No users found in the database."}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

@router.post('/create_test/', tags=['test'], status_code=status.HTTP_201_CREATED)
async def create_test(test:TestBase, db:db_dependency):
  db_test = Test(**test.model_dump()) #.model_dump() is a method in TestBase class that converts the Pydantic model to a dictionary without the need to specify each field or convert it manually.
  db.add(db_test)
  db.commit()

@router.get('/get_all_tests', tags=['test'], status_code=status.HTTP_200_OK)
async def get_all_tests(db:db_dependency):
  return db.query(Test).all()

# Example of a route with a query parameter
# Example: http://localhost:8000/test/greet/?name=John
# A query parameter is a key-value pair that is appended to the end of a URL.
# In this case, the key is 'name' and the value is 'John'.
# The query parameter is used to pass data to the server.
@router.get('/greet/', tags=['test'], status_code=status.HTTP_200_OK)
async def greet(name:str):
  return {'message': f'Hello {name}'}


# Example of a route with a path parameter
# Example: http://localhost:8000/test/greet/John
# A path parameter is a variable that is part of the URL path.
# In this case, the path parameter is 'name'.
# The path parameter is used to pass data to the server.
@router.get('/greet/{name}', tags=['test'], status_code=status.HTTP_200_OK)
async def greet_path(name:str):
  return {'message': f'Hello {name}'}

# Example of a route with a path parameter and a query parameter  
# Example: http://localhost:8000/test/greet/John?age=25
# A path parameter is a variable that is part of the URL path.
# In this case, the path parameter is 'name'.
# The path parameter is used to pass data to the server.
# A query parameter is a key-value pair that is appended to the end of a URL.
# In this case, the key is 'age' and the value is '25'.
# The query parameter is used to pass data to the server.
@router.get('/greet/{name}', tags=['test'], status_code=status.HTTP_200_OK)
async def greet_path_query(name:str, age:int):
  return {'message': f'Hello {name}, you are {age} years old'}

# Example of a route with dependency injections'
# Dependencies are objects that are passed to a route function by FastAPI.
# Dependencies can be used to inject objects such as database connections, configuration settings, etc.
# In this example, we are injecting a database connection object into the route function.
@router.get('/get_user', tags=['test'], status_code=status.HTTP_200_OK)
async def get_user(db:db_dependency):
  return db.query(User).all()

# Example of a route with multiple dependency injections from different sources
# In this example, we are injecting a database connection object and a configuration object into the route function.
@router.post('/get_test_config', tags=['test'], status_code=status.HTTP_200_OK)
async def get_user_config(db: Session = Depends(get_db), config: dict = Body(...)):
    users = db.query(Test).all()
    return {'config': config, 'users': users}



# Example of a route with a response model
# Response models are used to define the structure of the response that the route will return.
# Define a response model
# Defined in Backend/models/pydantic_models.py:
# class GreetResponse(BaseModel):
#     message: str
#     name: str

# Use the response model in the route function
@router.get('/greet_response/{name}', response_model=GreetResponse, tags=['test'], status_code=status.HTTP_200_OK)
async def greet_response(name:str):
  return GreetResponse(message=f'Hello {name}', name=name)

# Example of a route that returns a JSON response
# The response will be in JSON format
@router.get('/json_response', tags=['test'], status_code=status.HTTP_200_OK)
async def json_response():
  return {'message': 'This is a JSON response'}

# Example of a route that returns an HTML response
# The response will be in HTML format
@router.get('/html_response', tags=['test'], status_code=status.HTTP_200_OK)
async def html_response():
  return HTMLResponse(content='<h1>This is an HTML response</h1>', status_code=200)

# Example of a route that returns a custom response
# The response will be in plain text format
@router.get('/custom_response', tags=['test'], status_code=status.HTTP_200_OK)
async def custom_response():
  return 'This is a custom response'


# Example of a route that returns a custom response with a custom status code
# The response will be in plain text format
# The status code will be 201 (Created)
@router.get('/custom_response_status', tags=['test'], status_code=status.HTTP_201_CREATED)
async def custom_response_status():
  return 'This is a custom response with a custom status code'

# Example of a route that returns a custom response with a custom status code and headers
# The response will be in plain text format
# The status code will be 201 (Created)
# The response will include custom headers
@router.get('/custom_response_headers', tags=['test'], status_code=status.HTTP_201_CREATED)
async def custom_response_headers():
  return 'This is a custom response with custom headers', {'X-Custom-Header': 'Custom Value'}


# Example of a route that requires authentication via a token or API key
# The route will return a 401 (Unauthorized) status code if the authentication fails
# The route will return a 200 (OK) status code if the authentication succeeds

# Define a dependency to check the auth token
def get_token(token: str = Header(...)):
    valid_token = "1234567890"  # Example hardcoded token
    if token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication token"
        )
    return token

@router.get('/protected_route', tags=['test'], status_code=status.HTTP_200_OK)
async def protected_route(token: str = Depends(get_token)):
    # You can access the token here if needed, for example, logging or further validation
    return {'message': 'This is a protected route', 'token': token}

# Example of a route that requires authentication via headers
# The route will return a 401 (Unauthorized) status code if the authentication fails
# The route will return a 200 (OK) status code if the authentication succeeds
# Define a dependency to check the auth token
def check_auth_token(auth_token: str = Header(...)):
    valid_token = "securetoken123"  # Example hardcoded token
    if auth_token != valid_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication token"
        )
    return auth_token

@router.get('/secure_data', tags=['test'], status_code=status.HTTP_200_OK)
async def get_secure_data(
    auth_token: str = Depends(check_auth_token)
):
    # Assuming the token is valid, return the secure data
    secure_data = {
        "message": "This is secure data",
        "token": auth_token
    }
    return secure_data


# Suppose you are working with a database model for a User that has fields like id, created_at, and updated_at, 
# which should be automatically managed by the database. However, when creating a new user, 
# the client only needs to provide the name and email.
  
# To achieve this, you can define a Pydantic model that includes only the fields that the client needs to provide,
# and then use a function to create a new user instance with the required fields.

# Define a Pydantic model for creating a new user
# Defined in Backend/models/pydantic_models.py:
class UserCreate(BaseModel):
     name: str
     email: str

# Define a function to create a new user instance
# The function takes the user data from the client and creates a new user instance with the required fields
def create_new_user(user_data: UserCreate):
    new_user = User(
        name=user_data.name,
        email=user_data.email
    )
    return new_user

# Example of a route that creates a new user
# The route receives the user data from the client and creates a new user instance
@router.post('/create_user', tags=['test'], status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if a user with the same email already exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )
    # Create a new user instance with the required fields
    new_user = create_new_user(user_data)
    # Save the new user instance to the database
    # db.add(new_user)
    # db.commit()
    return {
       "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "created_at": new_user.created_at
    }

# Example of a route with optional query parameters
# The route receives optional query parameters from the client
# The query parameters are used to filter the results
@router.get('/users', tags=['test'], status_code=status.HTTP_200_OK)
async def get_users(
    name: str = None,
    email: str = None,
    db: Session = Depends(get_db)
):
    # Initialize a query to retrieve all users
    query = db.query(User)
    # Filter the results based on the query parameters
    if name:
        query = query.filter(User.name == name)
    if email:
        query = query.filter(User.email == email)
    # Retrieve the filtered results
    users = query.all()
    return users
