from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserRequest(BaseModel):
     email:EmailStr
     password:str


class UserResponse(BaseModel):
     email:EmailStr
     id: int
     created_at:datetime
     
     class Config:
          orm_mode = True


class UserLogin(BaseModel):
     email:EmailStr
     password:str

class PostBase(BaseModel):
    title:str 
    content:str
    published:bool = True

class PostCreate(PostBase):
    pass

class PostResponse(BaseModel):
    id:int
    title:str 
    content:str
    published:bool
    created_at:datetime
    user_id:int
    user:UserResponse
    class Config:
          from_attributes = True #orm_mode is deprecated

class PostVoteResponse(BaseModel):
     Post:PostResponse
     votes:int


class Token(BaseModel):
     access_token:str
     token_type:str

class TokenData(BaseModel):
    id:Optional[int] = None

class VoteIn(BaseModel):
     post_id:int
     dir:int