from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.config import settings
from app.models.user import User


def test_create_user(client: TestClient, db: Session) -> None:
    r = client.post(
        f"{settings.API_V1_STR}/register/",
        json={
            "email": "test@user.com",
            "password": "password123",
            "full_name": "Test User",
        },
    )

    assert r.status_code == 200

    data = r.json()

    user = db.exec(select(User).where(User.id == data["id"])).first()

    assert user
    assert user.email == "test@user.com"
    assert user.full_name == "Test User"


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER_EMAIL,
        "password": "incorrect",
    }
    r = client.post(f"{settings.API_V1_STR}/login", data=login_data)
    assert r.status_code == 400
