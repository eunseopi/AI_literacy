from fastapi import APIRouter, Depends, HTTPException
from src.database import crud
from src.models import models
from src.database.conn import get_db
from sqlalchemy.orm import Session


register_router = APIRouter()


@register_router.post("/register")
def create_user(user: models.UserCreate, db: Session = Depends(get_db)) -> models.User:
    """_summary_

    Args:
        method post\n
        body
        {
            "email": str ,
            "password": str ,
            "profile_image_url": str
            "nick_name": str
        }
        이미지url은 선택사항이고 로컬에서 사진 업로드하는 건 아직.. 안됨... 웹 url만 가능
    Raises:
        HTTPException: _description_

    Returns:
        models.User

        {
            "email": "string",
            "profile_image_url": "string",
            "nick_name": "string",
            "id": 0,
            "is_active": true,
            "created_at": "string",
            "continuous_day": 0
        }
    """
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    return crud.create_user(db, user)
