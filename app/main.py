from fastapi import Body, Depends, FastAPI, Response, status, HTTPException
from typing import Optional, List
import psycopg
from psycopg.rows import dict_row
from . import models
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .routers import posts, users, authentication, votes
from .config import settings

import time


# commenting it out because we are using alembic now 
# models.Base.metadata.create_all(bind=engine)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

         
app = FastAPI()

# while True:
#     try:
#         conn = (psycopg.connect("host=localhost  dbname=fastapi user=postgres password=haris", row_factory=dict_row ))
#         cursor = conn.cursor()
#         print ("connection succeededddd")
#         break
#     except Exception as error:
#         print ("failed to connect db")
#         print (error)
#         time.sleep(2)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(authentication.router)
app.include_router(votes.router)

print("harissss")

print(settings.database_username)

@app.get("/")
def root():
    return {"message": "Haris "}

# @app.get("/ ")
# def test_posts(db:Session = Depends(get_db)):
#     # posts = cursor.execute(""" SELECT * from "Posts" """).fetchall()
    
#     # print(posts)
#     posts = db.query(models.Post).all()
#     return {"posts" : posts}


