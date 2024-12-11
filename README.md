# Applyticz

# About
Applyticz is a web application that allows users to manage, track, and analyze their job applications. Users can connect their Gmail/Outlook accounts to enable automated tracking. After submitting an application to a company and recieving a confirmation email, application data will be parsed, organized, and added to their applications page. Users can then track this application through response, interview, and offer stages as they progress through the interview process.

Users also have access to a metrics page where they can gain statistical insights about their job search. Applyticz generates detailed reports on which applications provide the highest interview and response rates, as well as other numerical data.


# FastAPI Backend Setup

This is a basic FastAPI backend setup inside the `Backend` directory.

## Project Structure

```
Backend/
    app/
    ├── __init__.py
    ├── db/
    │   ├── __init__.py
    │   ├── database.py
    ├── models/
    │   ├── __init__.py
    │   ├── database_models.py
    │   ├── pydantic_models.py
    ├── routers/
    │   ├── __init__.py
    │   ├── auth_router.py
    │   ├── test_router.py
    ├── tests/
    │   ├── __init__.py
    │   ├── conftest.py
    │   ├── test_suite.py
    ├── utils/
    │   ├── __init__.py
    │   ├── utils.py
    ├── main.py
    ├── .venv
├── alembic/
    ├── versions/
    ├── env.py
├── .gitignore
├── alembic.ini
├── README.md
├── requirements.txt
├── .env (Hidden from Github)
├── run.sh
├── docker_backend.sh
├── Dockerfile
├── docker-compose.yml
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
```

### 2a. Use the run.sh Script

#### Run the backend script to automate the process of steps 2-4:

#### Grant executable permissions: Run the following command to allow execution of the script:
```bash
chmod +x run.sh
```

```bash
./run.sh
```

### 2. Create and activate the virtual environment

#### Create the virtual environment:
```bash
cd Backend
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
pip install -r requirements.txt|| pip3 install -r requirements.txt
```

### 4. Running the FastAPI Application

To start the FastAPI app with `main.py`:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Access the app at `http://127.0.0.1:8000`.

### 5. Add `.gitignore`

Include the following in `.gitignore` to avoid committing unnecessary files:

```
# Virtual environment
.venv/

# Python bytecode
__pycache__/

# .env file
.env
```

### 6. Add the .env file

Include the following in the .env file within the Backend directory:

```
DATABASE_URL=postgresql://user:password@localhost:5432/dbname
SECRET_KEY=your_secret_key
JWT_ALGORITHM=HS256
```

## Updating Routes

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

1. Write or update tests located in the `app/tests/` directory.

2. Run the tests to ensure everything works correctly:

#### Activate the virtual environment:
- **Linux/MacOS:**
- start from backend main directory
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
pip install -r requirements.txt || pip3 install -r requirements.txt
```

```bash
pytest app/tests/test_suite.py
```

Individual tests can be run with:
```bash
pytest app/tests/test_suite.py::test_function_name
```



# Developer Team

**Contributors:**
- Alec-Nesat Colak
- Dylan DePasquale
- Alejandro Androuin
- Pranav Venu

