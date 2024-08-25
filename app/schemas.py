from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import List, Optional



class UserBase(BaseModel):
    email: EmailStr
    password: str    

class UserCreate(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0,le=1)  # type: ignore


class PostBase(BaseModel):
    title: str
    content: str
    published: bool

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostOut(PostBase):
    created_at: datetime
    id: int
    owner_id: int
    owner: UserOut
    
class PostWithVotes(BaseModel):
    Post: PostOut
    votes: int


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None


