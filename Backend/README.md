
# FastAPI Backend Setup

This is a basic FastAPI backend setup inside the `Backend` directory.

## Project Structure

```
Backend/
│
├── .venv/             # Virtual environment (not committed to Git)
├── main.py            # Main FastAPI application
├── .gitignore         # Git ignore file to exclude unnecessary files
└── README.md          # Project documentation
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd Backend
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
pip install "fastapi[standard]" uvicorn
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
