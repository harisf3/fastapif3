import pytest
from app import models

@pytest.fixture()
def test_vote(test_posts, session, test_user):
    new_vote = models.Vote(post_id=test_posts[0].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()
    return new_vote


def test_vote_on_post(authorized_client, test_posts):
    data = {"post_id":test_posts[2].id, "dir":1}
    response = authorized_client.post("/votes/" , json=data)
    assert response.status_code == 201

def test_vote_down_on_post(authorized_client, test_posts, test_vote, session):
    data = {"post_id":test_vote.post_id, "dir":0}
    response = authorized_client.post("/votes/" , json=data)
    assert response.status_code == 201
    assert session.query(models.Vote).first() == None


def test_vote_on_post_unauthroized(client, test_posts, session):
    data = {"post_id":test_posts[2].id, "dir":1}
    response = client.post("/votes/" , json=data)
    assert response.status_code == 401

    