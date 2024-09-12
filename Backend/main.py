from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from database import get_db
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from models.database_models import User
from routers import test_router

app = FastAPI()

# if you want to create new routes for specific endpoints (e.g. /admin, /users, /items, etc) use app.include_routers(<filename>.router, '/<prefix>')
app.include_router(test_router.router, prefix='/test')


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Example endpoint template
# @app.get('/test')
# def test_(dependencies):
    #     pass  # Placeholder for actual dependency injection logic
    #     return {"message": "Hello, World!"}

@app.get("/")
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