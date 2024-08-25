from typing import List, Optional
from .. import models, oauth2,schemas
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
from sqlalchemy import func

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)



@router.get('/', response_model=List[schemas.PostWithVotes])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ''):

    results = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results



@router.get('/{id}',status_code=status.HTTP_201_CREATED,response_model=schemas.PostWithVotes)
def get_post(id:int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    result = db.query(models.Post,func.count(models.Vote.post_id).label('votes')).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id {id} is not found')
    
    return result



@router.post('/', response_model=schemas.PostOut)
def create_post(post:schemas.PostCreate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post



@router.put('/{id}',status_code=status.HTTP_202_ACCEPTED, response_model=schemas.PostOut)
def update_post(id:int, post:schemas.PostUpdate, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    updated_post = post_query.first()

    if updated_post is  None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id {id} does not exist')
    
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=403)
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()



@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f'Not authorized to perform requested action')

    post_query.delete(synchronize_session=False)
    db.commit()

    return {}
