from fastapi import APIRouter, Depends, HTTPException
from src.database import crud
from src.models import models
from src.database.conn import get_db
from sqlalchemy.orm import Session
from src.database import db_models


login_router = APIRouter()


@login_router.post("/login")
def login(user:models.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """_summary_

    Args:
        method post
        { "email": str , "plain_password": str }
    Raises:
        HTTPException: _description_

    Returns:
        models.User 
        { "id": int, "email": str, "is_active": bool, "created_at": str}
    """
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="로그인 정보가 일치하지 않습니다.")
    return db_user


