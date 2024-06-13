from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from fastapi import Depends
#! path 수정 sys.path.append("")
from src.database.conn import get_db
from src.main import app
from src.models import models
from src.database import crud

client = TestClient(app)


def test_login(db: Session = Depends(get_db)):
    # Create a test user
    user = models.UserCreate(email="test@example.com", plain_password="password")
    crud.create_user(db, user)

    # Test successful login
    response = client.post("/login", json={"email": "test@example.com", "plain_password": "password"})
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

    # Test incorrect login
    response = client.post("/login", json={"email": "test@example.com", "plain_password": "wrong_password"})
    assert response.status_code == 400
    assert response.json()["detail"] == "로그인 정보가 일치하지 않습니다."
    
    