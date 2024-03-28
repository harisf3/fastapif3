from app import schemas

def test_get_posts(authorized_client, test_posts):
    # print("headers")
    # print(authorized_client.headers)
    response = authorized_client.get("/posts/")
    
    # print("print response")
    # print (response.json()) 

    def validate(post_dict):
        return schemas.PostResponse(**post_dict)

    map(validate, response.json())
    
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)

def test_unathorized_user_get_posts(client, test_posts):
    response = client.get("/posts/")
    assert response.status_code == 401


def test_unathorized_user_get_one_post(client, test_posts):
    response = client.get(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401 

def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/8888")
    print(response)
    assert response.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f"/posts/{test_posts[0].id}")
    print (f"printing response {response.json()}")
    postResponse = schemas.PostVoteResponse(**response.json())
    
    assert response.status_code == 200
    assert postResponse.Post.id == test_posts[0].id

def test_delete_post_unauthorized(client, test_posts):
    response = client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_delete_post_authorized(authorized_client, test_posts):
    response = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert response.status_code == 204