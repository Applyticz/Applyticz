
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
pip || pip3 install -r requirements.txt
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


# Alembic for Database Migrations in FastAPI

This guide will help you manage database schema changes using Alembic in a FastAPI project. Follow the steps below to update your database models and apply the corresponding migrations to your database.

## Prerequisites

Ensure you have Alembic installed in your project. You can install it with:

```bash
pip install alembic
```

Also, ensure that Alembic has been initialized in your project. If not, run:

```bash
alembic init alembic
```

This will create an `alembic/` directory containing the Alembic configuration and migration environment.

## Steps for Updating Database Models

### Step 1: Modify Your Database Models
Navigate to the directory containing your database models (e.g., `models/database_models.py`) and update the existing models or add new ones.

For example, to add a new `User` model:

```python
from sqlalchemy import Column, Integer, String
from app.database import Base

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
```

### Step 2: Generate a New Migration
Once you've added or modified the model, create a migration to reflect the changes in your database schema. Use the following command to autogenerate a migration:

```bash
alembic revision --autogenerate -m "Add new User model"
```

This will create a migration script based on the changes in your SQLAlchemy models. The `-m` flag allows you to specify a descriptive message for the migration.

### Step 3: Review the Migration Script
Alembic will create a new migration script in the `alembic/versions/` folder. It's good practice to review the script to ensure it accurately represents the changes you've made to your models.

### Step 4: Apply the Migration
Once you're satisfied with the migration script, apply it to your database using:

```bash
alembic upgrade head
```

This command will update your database schema to the latest version, applying the newly created migration.

### Step 5: Downgrade Migration (if needed)
If you need to undo the migration, you can downgrade it with:

```bash
alembic downgrade -1
```

This command will revert the database schema to the previous version.

## Managing Alembic Files

### Files to Include in Version Control
- **`alembic/versions/`**: This folder contains migration scripts and should be included in version control (e.g., GitHub) so that all team members can track schema changes.
- **`alembic.ini`**: The Alembic configuration file, which contains database connection settings (using environment variables for sensitive data like `DATABASE_URL`).

### Files to Ignore
- **`alembic/__pycache__/`**: Byte-compiled files should be ignored in `.gitignore`.

## Quick Alembic Commands
- **Autogenerate a migration**: `alembic revision --autogenerate -m "Your migration message"`
- **Apply a migration**: `alembic upgrade head`
- **Downgrade a migration**: `alembic downgrade -1`

## Example Workflow
1. **Add or update models** in your `models/database_models.py` or relevant files.
2. **Generate a new migration** with `alembic revision --autogenerate -m "Your message"`.
3. **Review the migration** script.
4. **Apply the migration** to the database with `alembic upgrade head`.

By following these steps, you can ensure that your database schema stays in sync with your application's models.


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