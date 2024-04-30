from sqlalchemy.orm import Session
from src.database import db_models
from src.models import models 
from src.security.hash_password import HashPassword
from sqlalchemy.sql import func

hash_password = HashPassword()

def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()

def get_user_id_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first().id


def create_user(db: Session, user: models.UserCreate):
    hashed_password = hash_password.create_hash(user.password)
    db_user = db_models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    db_user = get_user_by_email(db, email)
    if not db_user:
        return False
    if not hash_password.verify_password(password, db_user.hashed_password):
        return False
    return db_user

def get_scores_by_user(db: Session, user_id: int):
    return db.query(db_models.Score).filter(db_models.Score.user_id == user_id).all()


def get_avg_score_by_user(db: Session, user_email: str):
    user_id = get_user_id_by_email(db, user_email)
    score = db.query(db_models.Score).filter(db_models.Score.user_id == user_id).all()
    score_sum = 0

    for i in range(len(score)):
        score_sum += score[i].score
        score_avg = score_sum / len(score)
    return score_avg


def save_score(db: Session, score: models.ScoreCreate,user_email:str):
    
    user_id = get_user_id_by_email(db, user_email)
    db_score = db_models.Score(**score.model_dump(),user_id=user_id)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score