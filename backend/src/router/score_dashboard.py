from fastapi import APIRouter, Depends, HTTPException
from src.database import crud
from src.models import models
from src.database.conn import get_db
from sqlalchemy.orm import Session


score_dashboard_router = APIRouter()


@score_dashboard_router.get("/avg_scores")
async def get_avg_scores(user_email: str, db: Session = Depends(get_db)):
    average = crud.get_avg_score_by_user(db, user_email)
    
    return {"average": average}