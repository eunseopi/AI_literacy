from fastapi import APIRouter, Depends, HTTPException
from src.database import crud
from src.models import models
from src.database.conn import get_db
from sqlalchemy.orm import Session


register_router = APIRouter()

@register_router.post("/register")
def create_user(user: models.UserCreate, db: Session = Depends(get_db))-> models.User:
    """_summary_

    Args:
        method post
        user{ "email": str , "password": str }
    Raises:
        HTTPException: _description_

    Returns:
        models.User 
        { "id": int, "email": str, "is_active": bool, "created_at": str}
    """
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    return crud.create_user(db, user)



    
    
    
    