from fastapi.testclient import TestClient 
from app.main import app 
from app import schemas 

client = TestClient(app)

def test_root():
    res = client.get("/")
    print(res.json().get('message'))
    assert res.json().get('message') == ("welcome to Lauben's API!: Proceed to /docs to perform requests")


def test_create_user():
    res = client.post("/users/", json={"email": "uganda@gmail.com", "password": "uganda"})
    # print(res.json())
    new_user = schemas.UserOut(**res.json()) # Unpack the dictionary
    assert new_user.email == "uganda@gmail.com"
    # assert res.json().get("email") == "uganda@gmail.com"
    assert res.status_code == 201