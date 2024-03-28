from app import schemas
import pytest
from jose import jwt
from app.config import settings




# def test_root(client): 
#     response = client.get("/")
#     assert  response.status_code ==  200
#     # assert response.json().get("message") == "Fast API by Haris"


def test_create_user(client):
    response = client.post("users/create", json={"email":"haris@gmail.com", "password":"1234567890"})
    user = schemas.UserResponse(**response.json())
    assert user.email == "haris@gmail.com"
    assert response.status_code == 201 


def test_login_user(client, test_user):
     
     response = client.post("/login", data={"username":test_user["email"], "password":test_user["password"]})  
     token = schemas.Token(** response.json())
     payload = jwt.decode(token.access_token, key=settings.secret_key, algorithms=[settings.algorithm])   
     user_id = payload.get("userid")
     assert test_user["id"] == user_id
     assert response.status_code == 200
     assert token.token_type == "bearer"

@pytest.mark.parametrize("email, password, status_code", [("wrongemail@gmail.com","1234567890", 403),
                                                          ("haris@gmail.com","wrong password", 403),
                                                          (None,1234567890, 422 )
])
def test_incorrect_login(client, test_user, email, password, status_code):
     
     response = client.post("/login", data={"username":email, "password":password}) 

     assert response.status_code == status_code

