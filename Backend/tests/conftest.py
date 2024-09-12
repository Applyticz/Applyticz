from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/../')  # Adjust this path if necessary

from main import app
from database import Base, get_db, DATABASE_URL
from models.database_models import User



@pytest.fixture(scope="module")
def overrideDbDepend(dbSession):
    app.dependency_overrides[get_db] = lambda: dbSession
    yield
    app.dependency_overrides.pop(get_db, None)
    
@pytest.fixture(scope="module")
def testClient():
    with TestClient(app) as client:
        yield client
        
@pytest.fixture(scope="module")
def dbSession():
    engine = create_engine(DATABASE_URL.replace('@db', '@localhost'))
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    connection = engine.connect()
    transaction = connection.begin()
    Base.metadata.bind = engine
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal(bind=connection)

    # delete all data before starting tests
    db.query(User).delete()
    db.commit()

    yield db

    transaction.rollback()
    connection.close()