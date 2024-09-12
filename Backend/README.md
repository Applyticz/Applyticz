
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

## Endpoints

- **GET /**: Returns a welcome message.


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

3. If you're adding a new model, you may need to create a migration using Alembic or your chosen migration tool.

```bash
alembic revision --autogenerate -m "Add new User model"
alembic upgrade head
```


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