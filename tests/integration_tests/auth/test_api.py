import pytest

from src.services.auth import AuthService
from src.api.dependencies import get_db,async_session_maker
from src.utils.db_manager import DBManager

async def test_flow_auth(db,ac):
    # Регистрация
    registration_new_user = await ac.post(
        "/auth/register",
        json={
            "email": "email2@example.com",
            "password": "password2",
        }
    )
    assert registration_new_user.status_code == 200

    # Аутентификация
    login_new_user = await ac.post(
        "/auth/login",
        json={
            "email": "email2@example.com",
            "password": "password2",
        }
    )

    assert login_new_user.status_code == 200

    cookie_token = ac.cookies.get("access_token")
    assert cookie_token

    # Проверка себя
    info_about_login_user = await ac.get(
        "/auth/me",
    )

    assert info_about_login_user.status_code == 200

    # Выход из профиля
    logout_user = await ac.post(
        "/auth/logout",
    )

    assert logout_user.status_code == 200
    assert not ac.cookies.get("access_token")

    # Проверка себя
    info_about_logout_user = await ac.get(
        "/auth/me",
    )

    assert info_about_logout_user.status_code == 401
    assert not ac.cookies.get("access_token")
