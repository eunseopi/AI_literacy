from pydantic import BaseModel,Field
from datetime import datetime, timezone, timedelta



KST = timezone(timedelta(hours=9))

"""User model
    class User(Base):
        __tablename__ = "users"

        id = Column(Integer, primary_key=True)
        email = Column(String, unique=True, index=True)
        hashed_password = Column(String)
        is_active = Column(Boolean, default=True)
        # avg_score = Column(Integer,default=0)
        scores = relationship("Score", back_populates="user")
"""

    
class UserBase(BaseModel):
    email: str
    #! 추후 로컬에서 이미지를 받아서 저장할 수 있도록 수정
    profile_image_url: str | None = None

class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int 
    is_active: bool = True
    created_at: str | None = None
    
    class Config:
        orm_mode = True
        
    
"""Score model
    class Score(Base):
        __tablename__ = "scores"

        user_id = Column(Integer, ForeignKey("users.id"),primary_key=True)
        play_date = Column(Integer, primary_key=True)
        score = Column(Integer)
        comment = Column(String)
        user_summary = Column(String)
        llm_summary = Column(String)
        docurl = Column(String)
        user = relationship("User", back_populates="scores")
"""        
class ScoreBase(BaseModel):
    score: int
    comment: str
    user_summary: str
    llm_summary: str
    docurl: str


class ScoreCreate(ScoreBase):
    pass


class Score(ScoreBase):
    user_id: int
    play_date: str | None = None
    

    class Config:
        orm_mode = True