from .. import models,schemas,utils
from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    if db.query(models.Users).filter(models.Users.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=
                            f'User with email {user.email} already exist')

    hashed_pwd = utils.hash(user.password)
    user.password = hashed_pwd
    new_user = models.Users(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get('/{id}',response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {id} does not exist')
    
    return user