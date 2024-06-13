import os
from typing import Annotated
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from src.database import crud
from src.models import models
from src.database.conn import get_db
from src.database import db_models
from src.security import hash_password

load_dotenv(".env")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

login_router = APIRouter()


@login_router.post("/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)) -> models.Token:
    """_summary_

    Args:
        method post

        request body:
        form에 담겨 와야합니다.
        form의 구조는 다음과 같습니다.
        
            "username": str ,
            "password": str
        

    Raises:
        HTTPException: _description_

    Returns:
        로그인한 유저의 access_token이 리턴됩니다.
        
        {
            "access_token": "string", #이걸 세션에 저장해두고 사용하면 됩니다.
            "token_type": "bearer"
        }
    """
    db_user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="로그인 정보가 일치하지 않습니다.")
    crud.reset_continuous_days(db, db_user.email)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return models.Token(
        access_token=hash_password.create_access_token(
            subject=db_user.email, expires_delta=access_token_expires
        )
    )
    
