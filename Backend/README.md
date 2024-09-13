
# FastAPI Backend Setup

This is a basic FastAPI backend setup inside the `Backend` directory.

## Project Structure

```
Backend/
│
├── .venv/             # Virtual environment (not committed to Git)
├── models/            # Contains the database models of tables and the pydantic models for validation
├── routes/            # Contains routes file grouped by endpoint prefixes 
├── tests/             # Contains files associated with PyTest
├── database.py        # Creates a conncetion to the database
├── main.py            # Main FastAPI application
├── .gitignore         # Git ignore file to exclude unnecessary files
├── .requirements.txt  # Contains all python packages required 
├── .env               # Contain environment variables ans secrets (not committed to Git)
└── README.md          # Project documentation
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Backend
```

### 2a. Use the backend Script

#### Run the backend script to automate the process of steps 2-4:

#### Grant executable permissions: Run the following command to allow execution of the script:
```bash
chmod +x backend.sh
```

```bash
./backend.sh
```

### 2. Create and activate the virtual environment

#### Create the virtual environment:
```bash
python3 -m venv .venv
```

#### Activate the virtual environment:
- **Linux/MacOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  source .venv\Scripts\activate
  ```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip || pip3 install install -r requirements.txt
```

### 4. Running the FastAPI Application

To start the FastAPI app with `main.py`:

```bash
uvicorn main:app --reload
```

Access the app at `http://127.0.0.1:8000`.

### 5. Add `.gitignore`

Include the following in `.gitignore` to avoid committing unnecessary files:

```
# Virtual environment
.venv/

# Python bytecode
__pycache__/
```


## FastAPI Backend - Route Guide

## Overview

This guide explains how to create various routes in FastAPI using the `APIRouter()` class. The examples cover basic routes, database-connected routes, query/path parameters, authentication, and response customization.

### 1. **Basic Route Example**
A simple GET route that returns a message:
```python
@router.get('/testing_route', tags=['test'])
async def test():
    return {'message': 'Testing Route'}
```

### 2. **Database Connection Test**
A route to test the connection to the database by fetching the first user:
```python
@router.get("/test-db", tags=["test"])
def test_db_connection(db: Session = Depends(get_db)):
    user = db.query(User).first()
    if user:
        return {"status": "Database connected!", "user": user}
    else:
        return {"status": "No users found in the database."}
```

### 3. **Creating a Resource via POST**
A POST route to create a resource (e.g., a test record in the database):
```python
@router.post('/create_test/', tags=['test'], status_code=status.HTTP_201_CREATED)
async def create_test(test: TestBase, db: Session = Depends(get_db)):
    db_test = Test(**test.dict())
    db.add(db_test)
    db.commit()
    return {"message": "Test created successfully!"}
```

### 4. **Query and Path Parameters**
You can handle both query and path parameters with FastAPI:
- Query parameters:
```python
@router.get('/greet/', tags=['test'])
async def greet(name: str):
    return {'message': f'Hello {name}'}
```

- Path parameters:
```python
@router.get('/greet/{name}', tags=['test'])
async def greet_path(name: str):
    return {'message': f'Hello {name}'}
```

- Path + Query parameters:
```python
@router.get('/greet/{name}', tags=['test'])
async def greet_path_query(name: str, age: int):
    return {'message': f'Hello {name}, you are {age} years old'}
```

### 5. **Authentication with API Key**
A route that requires authentication via an API key:
```python
def get_token(token: str = Header(...)):
    valid_token = "1234567890"
    if token != valid_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    return token

@router.get('/protected_route', tags=['test'])
async def protected_route(token: str = Depends(get_token)):
    return {'message': 'Access granted', 'token': token}
```

### 6. **Custom Responses**
FastAPI allows you to customize the response type and status codes:
```python
@router.get('/html_response', tags=['test'])
async def html_response():
    return HTMLResponse(content='<h1>This is an HTML response</h1>', status_code=200)
```

You can also return custom responses with custom headers:
```python
@router.get('/custom_response_headers', tags=['test'])
async def custom_response_headers():
    return 'Custom response', {'X-Custom-Header': 'Custom Value'}
```

### 7. **Working with Databases and Models**
For routes that interact with database models and Pydantic models, here’s an example:
```python
@router.post('/create_user', tags=['test'])
async def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    new_user = User(name=user_data.name, email=user_data.email)
    db.add(new_user)
    db.commit()
    return {"id": new_user.id, "name": new_user.name, "email": new_user.email}
```

### 8. **Filtering with Optional Query Parameters**
A route that filters results based on optional query parameters:
```python
@router.get('/users', tags=['test'])
async def get_users(name: str = None, email: str = None, db: Session = Depends(get_db)):
    query = db.query(User)
    if name:
        query = query.filter(User.name == name)
    if email:
        query = query.filter(User.email == email)
    return query.all()
```

---

This guide provides a basic summary of creating routes with FastAPI. For further details, refer to the FastAPI documentation.


## Updating Pydantic Models

Pydantic models are used to validate data coming into your application. To update or add new Pydantic models:

1. Navigate to the directory where your Pydantic models are located (e.g., `app/models/pydantic/`).

2. Modify the existing models or create a new one based on your requirements.

Example:
```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
```

3. Ensure that any new fields are validated using Pydantic's built-in validators if necessary.

4. Import your new or updated Pydantic model in the relevant routes or services where you need data validation.


## Updating Database Models

Database models define how your data is structured in the database. To update or add new database models:

1. Navigate to the directory containing your database models (e.g., `app/models/db/`).

2. Modify the existing models or create new ones.

Example:
```python
from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, unique=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
```

This guide provides a basic summary of creating routes with FastAPI. For further details, refer to the FastAPI documentation.

### 3. **Adding a New Model and Creating Database Migrations**

When you add a new model to your FastAPI project, you need to ensure that your database schema is updated accordingly. To handle this, we use Alembic, a lightweight database migration tool.

Follow these steps to create and apply a new migration:

#### **Step 1: Update Your Models**
First, update or add your new model in the `models.py` or relevant file. For example, let's say you add the following `User` model:

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
```

#### **Step 2: Generate a New Migration**
Once you've added or modified the model, you need to create a migration to reflect these changes in the database schema. Use the following Alembic command to autogenerate the migration:

```bash
alembic revision --autogenerate -m "Add new User model"
```

This command will:
- **Autogenerate** the migration script based on the changes you've made to your SQLAlchemy models.
- The `-m` flag allows you to specify a meaningful message (e.g., "Add new User model").

#### **Step 3: Review the Migration Script**
Alembic will create a new migration script in the `migrations/versions` folder. It’s a good practice to review this script to ensure it accurately reflects the changes you want to apply to the database.

#### **Step 4: Apply the Migration**
Once you're satisfied with the migration script, apply the migration to your database by running:

```bash
alembic upgrade head
```

This command will update your database schema to the latest version (i.e., apply the migration you just created).

---

### **Quick Commands for Migrations:**
- **Autogenerate a migration**: `alembic revision --autogenerate -m "Your migration message"`
- **Apply the migration**: `alembic upgrade head`
- **Downgrade to a previous version** (if needed): `alembic downgrade -1`

By following these steps, you ensure that your database schema stays in sync with your models, reducing the chances of database errors or inconsistencies.


## Updating Routes

To update or add new routes in the application:

1. Navigate to the routes folder (e.g., `app/routes/`).

2. Create a new route or update an existing one based on your new model or logic.

Example:
```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.pydantic import UserCreate
from app.models.db import User
from app.db.session import get_db

router = APIRouter()

@router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```


## Testing the Changes

After updating the models or routes, always ensure to:

1. Write or update tests located in the `tests/` directory.

2. Run the tests to ensure everything works correctly:

#### Activate the virtual environment:
- **Linux/MacOS:**
  ```bash
  source .venv/bin/activate
  ```
- **Windows:**
  ```bash
  source .venv\Scripts\activate
  ```

#### If dependencies aren't already installed:
```bash
python -m pip install --upgrade pip
pip || pip3 install install -r requirements.txt
```

```bash
pytest tests/test_suite.py
```