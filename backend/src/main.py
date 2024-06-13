from dotenv import load_dotenv
import secrets
import os

import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.middleware.cors import CORSMiddleware
from src.router import (
    llm_router,
    score_dashboard_router,
    login_router,
    register_router,
    profile_router,
)
from src.database.conn import engine
from src.database import db_models


# 네이버 뉴스기사 주소


"""summary_of_function
    1. 요약할 문서 제시
    2. 문서를 사용자가 요약
    3. 사용자의 입력을 gpt input에 넣고 gpt가 요약한 결과와 비교
    4. 점수나 결과를 반환
"""

env = os.getenv("ENV", "")
load_dotenv(f".env{env}")
ADMIN_USER, ADMIN_PASSWORD = os.getenv("ADMIN_USER"), os.getenv("ADMIN_PASSWORD")


db_models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)


# swagger 문서 보안
security = HTTPBasic()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    # compare_digest : 문자열 비교시 타이밍 공격을 방지하기 위한 함수
    correct_username = secrets.compare_digest(credentials.username, ADMIN_USER)
    correct_password = secrets.compare_digest(credentials.password, ADMIN_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


@app.get("/docs", include_in_schema=False)
async def get_swagger_documentation(username: str = Depends(get_current_username)):
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
async def get_redoc_documentation(username: str = Depends(get_current_username)):
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
async def openapi(username: str = Depends(get_current_username)):
    return get_openapi(title=app.title, version=app.version, routes=app.routes)


origins = ["*"]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(llm_router)
app.include_router(score_dashboard_router)
app.include_router(login_router)
app.include_router(register_router)
app.include_router(profile_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
