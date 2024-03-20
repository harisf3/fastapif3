from fastapi import APIRouter, status, Depends, HTTPException

from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2

router = APIRouter(
    prefix="/votes",
    tags=["Votes"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote_post(vote:schemas.VoteIn, db:Session = Depends(get_db), 
              current_user:models.User = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post does not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, 
                                              models.Vote.user_id == current_user.id)
    
    find_vote = vote_query.first()
    if (vote.dir == 1):
        if find_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="vote already added")
        new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "vote added succesfully"}
    else :
        if find_vote == None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="vote does not exist")
        vote_query.delete(synchronize_session = False)
        db.commit()
        return {"message": "vote deleted succesfully"}


