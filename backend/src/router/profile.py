from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlalchemy.orm import Session
from src.database import crud
from src.database.conn import get_db
from src.models import models
from src.security.hash_password import get_current_user

profile_router = APIRouter()


@profile_router.get("/profile")
def get_user_profile(
    # user_email: str,
    current_user: Annotated[models.User, Depends(get_current_user)],
    db: Session = Depends(get_db),
) -> models.User:
    """_summary_

    Args:
        method get\n

        
        헤더에 이런식으로 넣어 주셔야 합니다.

        headers: {"Authorization" : `Bearer ${token}`}



    Raises:
        HTTPException: _description_

    Returns:
        models.User

        {
            "email": "test@abc.com",
            "profile_image_url": "https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png",
            "id": 1,
            "is_active": true,
            "created_at": "2024-05-20 23:52:02",
            "continuous_day": 1
            "nick_name": "익명"
        }
    """
    db_user = crud.get_user_by_email(db, current_user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="없는 유저입니다.")
    return db_user


@profile_router.post("/update_profile_img")
async def update_user_profile(
    update_img: dict, current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)
)->dict:
    """_summary_

    inputs:
        method post\n
        body
        {
            "update_img": str,
        }
        
        헤더에 이런식으로 넣어주셔야 합니다.
        
        headers: {"Authorization" : `Bearer ${token}`}

    Returns:

        {
            "updated_img": str
        }


    """

    db_user = crud.get_user_by_email(db, current_user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="없는 유저입니다.")

    updated_img = crud.update_user_profile_image(db, db_user.email, update_img["update_img"])

    return {"updated_img": updated_img}


@profile_router.post("/update_nickname")
async def update_user_nickname(
    update_nickname: dict, current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db)
)->dict:
    """_summary_

    inputs:
        method post\n
        body
        {
            "update_nickname": str,
        }
        
    Return:

        {
            "updated_nickname": str
        }
        
    """
    db_user = crud.get_user_by_email(db, current_user.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="없는 유저입니다.")

    updated_nickname = crud.update_user_nickname(db, db_user.email, update_nickname["update_nickname"])

    return {"updated_nickname": updated_nickname}