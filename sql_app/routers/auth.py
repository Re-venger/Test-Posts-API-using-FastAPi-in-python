from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schema, models, utils, Oauth2

router = APIRouter(
    tags=["Authentication"]
    )


@router.post("/login", response_model=schema.Token)
def login_user(user_cred: OAuth2PasswordRequestForm = Depends(),  db: Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_cred.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials. Check Your Email or Password")

    if not utils.verifyPass(user_cred.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials. Check Your Email or Password")


    # create the token 
    access_token = Oauth2.create_access_token(data={"user_id":user.id})



    print(user.id, user.email, end="\n")
    print(access_token)




    # return the token
    return {
        'access_token': access_token,
        "token_type": "bearer"
    }