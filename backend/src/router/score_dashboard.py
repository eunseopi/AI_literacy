from typing import Annotated,List,Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from src.security.hash_password import get_current_user
from src.database import crud
from src.models import models
from src.database.conn import get_db

score_dashboard_router = APIRouter()


@score_dashboard_router.get("/avg_scores")
async def get_avg_scores(current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db))->dict:
    """_summary_

    input:

        Args:
        method get\n
        
        헤더는 이런식으로 넣어 주셔야 합니다.
        
        headers: {"Authorization" : `Bearer ${token}`}
        
        
    Returns:

        {
            "average" : int
        }
    """
    average = crud.get_avg_score_by_user(db, current_user.email)

    return {"average": average}


@score_dashboard_router.get("/history")
async def get_summary_history(current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db))->List[models.Score]:
    """_summary_

    
    Input: 

        method get\n
        
        헤더에 이런식으로 넣어 주셔야 합니다.
    
        headers: {
            "Authorization" : `Bearer ${token}`
            }

        

    Returns:

        
        list
        

        list의 각각의 인덱스는 다음과 같은 형식을 가집니다.

        {
            "played_date": "2024-05-20",
            "score": 1,
            "user_summary": "안녕",
            "docurl": "https://news.sbs.co.kr/news/newsPlusList.do?themeId=10000000134&plink=SITEMAP&cooper=SBSNEWS",
            "user_id": 1,
            "comment": "제공된 요약은 문서의 내용과 관련이 없습니다. 요약이 문서의 주요 내용을 반영해야 합니다.",
            "llm_summary": "충남 아산의 현대병원 박현서 원장이 필리핀 이주노동자 A씨에게 아버지의 장례 참석을 위해 100만 원을 빌려주었고, A씨는 8개월 후 그 돈을 갚으며 감사의 편지를 전달했습니다. 이 사연은 많은 이들에게 감동을 주었으며, 박 원장과 A씨 모두 감정적인 재회를 경험했습니다."
        }


    """
    history = crud.get_scores_by_user(db, current_user.email)
    return history


@score_dashboard_router.get("/continuous_days")
async def get_continuous_days(current_user: Annotated[models.User, Depends(get_current_user)], db: Session = Depends(get_db))->dict:
    """_summary_

    Args:

        Args:
        method get\n
        
            헤더에 이런식으로 넣어 주셔야 합니다.

            headers: {"Authorization" : `Bearer ${token}`}
        
    Returns:

        {
            "continuous_days" : int
        }
    """
    continuos_days = crud.get_continuous_days(db, current_user.email)

    return {"continuous_days":continuos_days}
