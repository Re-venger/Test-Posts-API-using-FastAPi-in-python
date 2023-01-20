from typing import Optional
from pydantic import BaseModel
from datetime import datetime
from pydantic import EmailStr


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

#* Data model For Creating a Post
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


class UsersRes(BaseModel):
    id:int
    email: EmailStr
    dateCreated: datetime

    class Config:
        orm_mode = True


class Post(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    dateCreated: datetime
    user_id:int
    owner: UsersRes


    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    email: EmailStr
    password: str





class UserLogin(BaseModel):
    email:EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
    
