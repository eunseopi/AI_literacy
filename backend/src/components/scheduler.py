import time
from datetime import datetime,timezone,timedelta
from sqlalchemy.orm import Session
from src.database.conn import get_db
from fastapi import Depends
from apscheduler.schedulers.background import BackgroundScheduler
from . import news_content
from src.database import crud

KST = timezone(timedelta(hours=9))


def craw_scheduler(db: Session = next(get_db())):
    times = datetime.now(KST)   
    print("웹문서를 크롤링 합니다!")
    contents = news_content.get_news_contents()
    print(type(contents))
    print("asdasd",contents)
    try:
        today = datetime.now(KST).date().strftime("%Y-%m-%d")
        crud.save_content(db,content = contents,created_at = today)
    except Exception as e:
        print(e)
        
    print(times)
    
    

schedule = BackgroundScheduler(daemon=True, timezone='Asia/Seoul')
# schedule.add_job(craw_scheduler, 'interval', days=1)
schedule.add_job(craw_scheduler, 'cron', hour=0, minute=00)
schedule.start()
#-----


