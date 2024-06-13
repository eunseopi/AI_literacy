from sqlalchemy.orm import Session
from sqlalchemy import and_
from src.database import db_models
from src.models import models
from src.security.hash_password import HashPassword
from datetime import datetime, timezone, timedelta


KST = timezone(timedelta(hours=9))


hash_password = HashPassword()


def get_user_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first()


def get_user_id_by_email(db: Session, email: str):
    return db.query(db_models.User).filter(db_models.User.email == email).first().id


def create_user(db: Session, user: models.UserCreate):
    hashed_password = hash_password.create_hash(user.password)
    db_user = db_models.User(
        email=user.email,
        hashed_password=hashed_password,
        nick_name=user.nick_name,
        profile_image_url=user.profile_image_url,
    )
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


def get_scores_by_user(db: Session, user_email: int):
    user_id = get_user_id_by_email(db, user_email)
    return db.query(db_models.Score).filter(db_models.Score.user_id == user_id).all()


def get_avg_score_by_user(db: Session, user_email: str):
    score = get_scores_by_user(db, user_email)
    score_sum = 0

    score_avg = 0

    for i in range(len(score)):
        score_sum += score[i].score
        score_avg = score_sum / len(score)
    return score_avg


def save_score(db: Session, score: models.ScoreCreate, user_email: str):
    user_id = get_user_id_by_email(db, user_email)
    db_score = db_models.Score(**score.model_dump(), user_id=user_id)
    db.add(db_score)
    db.commit()
    db.refresh(db_score)
    return db_score


def test_save_score(db: Session, score: models.ScoreCreate, user_email: str):
    print("start update query!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    played_date = datetime.now(KST).date().strftime("%Y-%m-%d")
    user_id = get_user_id_by_email(db, user_email)
    db.query(db_models.Score).filter(and_((db_models.Score.user_id == user_id)&(db_models.Score.played_date == played_date))).\
        update({db_models.Score.score: score.score, db_models.Score.comment: score.comment, db_models.Score.user_summary: score.user_summary, db_models.Score.llm_summary: score.llm_summary})
    # db_score.append(db_models.Score(**score.dict(), user_id=user_id))
    # print("\n이거 뭥!!!!!!!!!!!!!!!!!!!!!!",db_score,"\n")
    # db_score = db_models.Score(**score.dict(), user_id=user_id)
    # db.add(db_score)
    db.commit()
    # db.refresh(db_score)
    return True




def save_content(db: Session, content: str, created_at: str):
    db_content = db_models.Contents(content=content, created_at=created_at)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content


def get_contents(db: Session):
    today = datetime.now(KST).date().strftime("%Y-%m-%d")
    content = (
        db.query(db_models.Contents)
        .filter(db_models.Contents.created_at == today)
        .all()
    )
    return content


def get_content_by_date(db: Session, created_at: str):
    content = db.query(db_models.Contents).filter(db_models.Contents.created_at == created_at).first()
    return content



def get_continuous_days(db: Session, user_email: str):
    user = db.query(db_models.User).filter(db_models.User.email == user_email).first()
    return user.continuous_day


def increase_continuous_days(db: Session, user_email: str):
    user_id = get_user_id_by_email(db, user_email)
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()

    today = datetime.now(KST).date()

    played_dates = get_scores_by_user(db, user_email)
    for i in range(len(played_dates)):
        played_dates[i] = played_dates[i].played_date
    played_dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

    recent_played_day = datetime.strptime(played_dates[-1], "%Y-%m-%d").date()

    print("asdasdasdasd", today, recent_played_day)

    if today == recent_played_day:
        user.continuous_day += 1
    else:
        if today - recent_played_day != timedelta(days=1):
            print("연속된 날짜가 아닙니다.")
            user.continuous_day = 0
        else:
            print("연속된 날짜입니다.")
            user.continuous_day += 1
    db.commit()
    db.refresh(user)
    return user.continuous_day


def reset_continuous_days(db: Session, user_email: str) -> int:
    user_id = get_user_id_by_email(db, user_email)
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()

    today = datetime.now(KST).date()

    played_dates = get_scores_by_user(db, user_email)
    for i in range(len(played_dates)):
        played_dates[i] = played_dates[i].played_date
    played_dates.sort(key=lambda date: datetime.strptime(date, "%Y-%m-%d"))

    if len(played_dates) == 0:
        user.continuous_day = 0
        return user.continuous_day

    recent_played_day = datetime.strptime(played_dates[-1], "%Y-%m-%d").date()

    print("asdasdasdasd", today, recent_played_day)

    if today == recent_played_day:
        pass
    else:
        if today - recent_played_day != timedelta(days=1):
            print("연속된 날짜가 아닙니다.")
            user.continuous_day = 0

    db.commit()
    db.refresh(user)
    return user.continuous_day


def update_user_profile_image(db: Session, user_email: str, profile_image_url: str):
    user_id = get_user_id_by_email(db, user_email)
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    user.profile_image_url = profile_image_url
    db.commit()
    db.refresh(user)
    return user.profile_image_url


def update_user_nickname(db: Session, user_email: str, nick_name: str):
    user_id = get_user_id_by_email(db, user_email)
    user = db.query(db_models.User).filter(db_models.User.id == user_id).first()
    user.nick_name = nick_name
    db.commit()
    db.refresh(user)
    return user.nick_name

