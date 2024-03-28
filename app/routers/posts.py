from fastapi import Body, Depends, Response, status, HTTPException, APIRouter
from typing import List
from .. import models, schemas, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

my_posts = [{"id":1, "title":"title of post 1", "content":"content of post1"} 
            ,{"id":2, "title":"title of post 2", "content":"content of post2"}]

def find_posts(id):
    for post in my_posts:
        if post["id"] == id :
            return post

def find_index(id:int):
    for i,post in enumerate(my_posts):
        if post["id"] == id:
            return i



@router.get("/", response_model=List[schemas.PostVoteResponse])
def get_posts(db:Session = Depends(get_db), user:models.User = Depends(oauth2.get_current_user), limit = 10, offset = 0):
    # posts = cursor.execute(""" SELECT * from "Posts" """).fetchall()
    # print(posts)
    # posts = db.query(models.Post).offset(offset).limit(limit).all()
    # posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).all()
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).offset(offset).limit(limit).all()
    print (posts) 
  
    return posts

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(new_post:schemas.PostCreate, db:Session = Depends(get_db), user :models.User = Depends(oauth2.get_current_user)):
    # post_dict = new_post.model_dump()
    # post_dict["id"] = len(my_posts) + 1
    # my_posts.append(post_dict)

    # cursor.execute("""INSERT INTO "Posts" (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (new_post.title, new_post.content, new_post.published))
    # new_post = cursor.fetchone()
    # conn.commit()

    # new_post = models.Post(title=new_post.title, content=new_post.content, published=new_post.published)
    print("user id is -----> ")
    print(user.id)
    new_post = models.Post(**new_post.model_dump())
    new_post.user_id = user.id
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

@router.get("/{id}", response_model=schemas.PostVoteResponse)
def get_post(id:int, response:Response, db:Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    # post = find_posts(id)
    # cursor.execute("""SELECT * FROM "Posts" where id = %s """, (str(id),))
    # new_post = cursor.fetchone()

    # new_post = db.query(models.Post).filter(models.Post.id == id).first()
    new_post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).where(models.Post.id == id).first()
    

    if not new_post:
        print("didn't get any post")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return new_post

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,  db:Session = Depends(get_db), current_user:models.User = Depends(oauth2.get_current_user)):
    # index = find_index(id=id)
    # cursor.execute("""DELETE FROM "Posts" where id = %s  returning * """, (str(id),))
    # index = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post:models.Post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="not authorized to delete")

    # my_posts.pop(index)
    # conn.commit() 
    post_query.delete(synchronize_session=False)
    db.commit()
    return {"message":"post deleted successfully"}

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(updated_post:schemas.PostCreate, id:int, db:Session = Depends(get_db)):
    # index = find_index(id=id)
    # if index == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    # new_post = post.model_dump()
    # new_post["id"] = id
    # my_posts[index] = new_post

    # cursor.execute("""UPDATE "Posts" set title = %s, content = %s, published =%s where id = %s RETURNING *""", (post.title, post.content, post.published, str(id )))
    # new_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    # conn.commit()
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit() 
    # db.d 
    return post_query.first()