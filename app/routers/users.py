from fastapi import Body, Depends, FastAPI, Response, status, HTTPException, APIRouter
from typing import Optional, List
from .. import models, schemas, utils
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserRequest, db:Session = Depends(get_db)):

    
    pwd_hashed = utils.hashed_password(user.password)
    user.password = pwd_hashed

    try : 
        new_user = models.User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user 
    
    except Exception as error:
        print(error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.get("/{id}", response_model=schemas.UserResponse)
def get_post(id:int, response:Response, db:Session = Depends(get_db)):

    new_user = db.query(models.User).filter(models.User.id == id).first()
    

    if not new_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id {id} does not exist")
        # response.status_code = status.HTTP_404_NOT_FOUND
    return new_user
