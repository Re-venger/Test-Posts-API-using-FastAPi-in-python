from fastapi.exceptions import HTTPException
from fastapi import status, Depends, APIRouter
from pydantic import BaseModel
from sqlalchemy.orm import Session
from typing import List
import psycopg2
from psycopg2.extras import RealDictCursor
from .. import models,schema
from ..database import engine, get_db
from datetime import datetime
from ..utils import *

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

# * Create a new User
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schema.UsersRes)
def create_user(user:schema.UserCreate, db: Session = Depends(get_db)):
    

    # hash the password
    user.password = hashPass(user.password)

    # , dateCreated=datetime.now()
    new_user = models.User(email=user.email, password=user.password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


#* get the user by his id
@router.get("/{id}", response_model=schema.UsersRes)
def get_user(id:int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User Not Found")
    
    return user



#* get all the users 
@router.get("/", response_model=List[schema.UsersRes])
def get_users(db: Session=Depends(get_db)):

    users_list = db.query(models.User).all()

    return users_list