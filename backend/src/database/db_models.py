from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from src.database.conn import Base 
from datetime import datetime, timezone, timedelta



KST = timezone(timedelta(hours=9))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    created_at = Column(String,  default=lambda: datetime.now(KST).strftime("%Y-%m-%d %H:%M:%S"))
    continuous_day = Column(Integer, default=0)
    # avg_score = Column(Integer,default=0)
    profile_image_url = Column(String, default="https://cdn.icon-icons.com/icons2/1378/PNG/512/avatardefault_92824.png")
    scores = relationship("Score", back_populates="user")
    
class Score(Base):
    __tablename__ = "scores"

    user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
    played_date = Column(String, default=lambda: datetime.now(KST).strftime("%Y-%m-%d"),primary_key=True)
    score = Column(Integer)
    comment = Column(String)
    user_summary = Column(String)
    llm_summary = Column(String)
    docurl = Column(String)
    user = relationship("User", back_populates="scores")


class Contents(Base):
    __tablename__ = "contents"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String)
    created_at = Column(String, default=lambda: datetime.now(KST).strftime("%Y-%m-%d"),primary_key=True)