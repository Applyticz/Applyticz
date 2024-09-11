from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from database import get_db
from sqlalchemy import text
from models import User

app = FastAPI()

# Example endpoint template
# @app.get('/test')
# def test_(dependencies):
    #     pass  # Placeholder for actual dependency injection logic
    #     return {"message": "Hello, World!"}


@app.get("/test")
def test():
    return {"message": "Hello, World!"}

@app.get("/test-db")
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