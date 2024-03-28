from fastapi. testclient import TestClient
from app.main import app
from app import schemas, models
from app.config import settings
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
from app.oauth2 import create_access_token
import pytest



SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"
# print("database url")
print (SQLALCHEMY_DATABASE_URL)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
     )
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base = declarative_base() 









@pytest.fixture()
def session():
    # command.upgrade("head") alembic command
    # command.downgrade("base") alembic downgrade
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()

    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    def get_override_db():
    
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] =  get_override_db
    
    yield TestClient(app)    


@pytest.fixture
def test_user(client):
    user_data = {"email":"haris@gmail.com", "password":"1234567890"}
    response = client.post("users/create",  json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"userid":test_user["id"]})

@pytest.fixture
def authorized_client(token, client):
    # print (f"token is {token}")
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_posts(session, test_user):
    # data = {"title":"haris", "content":"Test post in unit test"}
    # response = authorized_client.post("/posts/", json=data)
    # return models.Post(**response.json())
    posts_data=[{"title":"haris", "content":"Test post in unit test 1", "user_id":test_user['id']},
                {"title":"haris", "content":"Test post in unit test 2", "user_id":test_user['id']},
                {"title":"haris", "content":"Test post in unit test 3", "user_id":test_user['id']}]
    
    # one_post = {"title":"haris", "content":"Test post in unit test 1", "user_id":test_user['id']}
    # onePost = models.Post(**one_post)
    # print (f" one post {onePost.title}")

    def create_post_model(post_dict):
       return models.Post(**post_dict)

        

    post_map = map(create_post_model, posts_data)
   
    posts = list(post_map)
    # print ("posts--")
    # print (posts)
    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts