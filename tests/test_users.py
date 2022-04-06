from fastapi.testclient import TestClient 
import pytest 
from sqlalchemy import create_engine 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker
from app.database import get_db
from app.main import app 
from app.database import get_db 
from app import schemas 
from app.config import settings 
from app.database import Base 

# SQLALCHEMY_DATABASE_URL = f"postgresql://postgres:password123@localhost:5432/fastapi_test"

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test" 



engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Build all the tables based off the models
Base.metadata.create_all(bind=engine)


# Base = declarative_base()

# Dependency
def override_get_db(): # Call this function everytime we get a call to our API endpoints.
    # Everytime we get a request, we get a session
    db = TestingSessionLocal() # Allows to make queries using SQLAlchemy
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# client = TestClient(app)

@pytest.fixture 
def client():
    # run our code before we run our test
    # Base.metadata.create_all(bind=engine)
    # yield TestClient(app) # Return our TestClient instance 
    # run our code after our test finishes
    # Base.metadata.drop_all(bind=engine)

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)

    
def test_root(client):
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == ("welcome to Lauben's API!: Proceed to /docs to perform requests")


def test_create_user(client):
    res = client.post("/users/", json={"email": "uganda@gmail.com", "password": "uganda"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json()) # Unpack the dictionary
    assert new_user.email == "uganda@gmail.com"
    # assert res.json().get("email") == "uganda@gmail.com"
    assert res.status_code == 201