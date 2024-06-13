import os
from typing import Any, Annotated
import secrets
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.database.conn import get_db
from src.models import models
from src.database import crud


load_dotenv(".env")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
SERVER_URL = os.getenv("SERVER_URL")

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{SERVER_URL}/login")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    def create_hash(self, password: str):
        return pwd_context.hash(password)

    def verify_password(self, plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)


def create_access_token(subject: str | Any, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone(timedelta(hours=9))) + expires_delta
    to_encode = {"exp": expire, "sub": subject}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    token: Annotated[str, Depends(reusable_oauth2)], db: Session = Depends(get_db)
) -> models.User:
    print(token)
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        token_data = models.TokenPayload(**payload)
        print(token_data)
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401,detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401,detail="Invalid token")
    user = crud.get_user_by_email(db, token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
