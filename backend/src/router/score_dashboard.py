from fastapi import APIRouter, Depends, HTTPException
from src.database import crud
from src.models import models
from src.database.conn import get_db
from sqlalchemy.orm import Session
from datetime import datetime

score_dashboard_router = APIRouter()


@score_dashboard_router.get("/avg_scores")
async def get_avg_scores(user_email: str, db: Session = Depends(get_db)):
    """_summary_

    input:
    
        {
            "user_email" : str
        }  
    
    Returns:
    
        {
            "average" : int
        }
    """
    average = crud.get_avg_score_by_user(db, user_email)
    
    return {"average": average}


@score_dashboard_router.get("/history")
async def get_summary_history(user_email: str, db: Session = Depends(get_db)):
    """_summary_

    input:
    
        {
            "user_email" : str 
        }
    
    Returns:
    
        {
            "history" : list
        }
        
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
    history = crud.get_scores_by_user(db, user_email)
    return history


@score_dashboard_router.get("/continuous_days")
async def get_continuous_days(user_email: str, db: Session = Depends(get_db)):
    """_summary_

    Args:
    
        {
            "user_email" : str 
        }

    Returns:
    
        {
            "continuous_days" : int
        }
    """
    continuos_days = crud.get_continuous_days(db, user_email)
    
    return continuos_days

        
        