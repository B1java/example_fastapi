from fastapi import Depends, HTTPException, status
import jwt
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings 
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return jwt_token

def verify_access_token(token: str, cred_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_id = str(payload.get("user_id"))

        if token_id is None or token_id == 'None':
            raise cred_exception
        token_data = schemas.TokenData(id=token_id)
    except jwt.PyJWTError:
        raise cred_exception
    
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)):
    cred_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f'Could not validate credentials',headers={'WWW-Authnticate':'Bearer'})

    token = verify_access_token(token, cred_exception)

    user = db.query(models.Users).filter(models.Users.id == token.id).first()

    return user