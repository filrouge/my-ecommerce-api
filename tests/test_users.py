import pytest
from datetime import datetime
from werkzeug.security import check_password_hash
from app.models import User
from app.core.auth_utils import get_user_by_email

from typing import Tuple, Dict
from flask.testing import FlaskClient
from sqlalchemy.orm import Session

from app.core.auth_utils import decode_token

class TestUserRegister:

    @pytest.mark.parametrize("payload", [
        {"email": "test1@email.com", "nom": "Test1", "password": "123456"},
        {"email": "test2@email.com", "nom": "Test2", "password": "abcdef"}
    ])
    def test_new_user(self, test_client: Tuple[FlaskClient, Session],
                      payload: Dict) -> None:
        client, session = test_client

        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 201

        data = resp.get_json()
        assert data["message"] == "Client inscrit"
        assert data["user"]["email"] == payload["email"]
        assert data["user"]["role"] == "client"

        user = get_user_by_email(session, payload["email"])
        assert user is not None
        assert check_password_hash(user.password_hash, payload["password"])
        assert isinstance(user.date_creation, datetime)

    @pytest.mark.parametrize("payload", [
        {"email": "duplicated@email.com", "nom": "Duplicate", "password": "123456"},
    ])
    def test_duplicate_email(self,
                             test_client: Tuple[FlaskClient, Session],
                             payload: Dict) -> None:
        client, session = test_client
        client.post("/api/auth/register", json=payload)

        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "Adresse e-mail déjà utilisée"

        users = session.query(User).filter_by(email=payload["email"]).all()
        assert len(users) == 1


    @pytest.mark.parametrize("payload", [
        {"email": "email.com", "nom": "Test", "password": "123456"},
        {"email": "@email.com", "nom": "Test", "password": "123456"},
        {"email": "test@", "nom": "Test", "password": "123456"},
        {"email": "test@@email.com", "nom": "Test", "password": "123456"}
    ])
    def test_strange_email(self,
                             test_client: Tuple[FlaskClient, Session],
                             payload: Dict) -> None:
        client, session = test_client
        client.post("/api/auth/register", json=payload)

        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 422
        assert resp.get_json()[0]["loc"] == ["email"]
        assert "value is not a valid email address" in resp.get_json()[0]["msg"]

        user = session.query(User).filter_by(email=payload["email"]).one_or_none()
        assert user is None

    
    @pytest.mark.parametrize("payload", [
        {"email": "test@email.com", "nom": "Test", "password": "123"},
        {"email": "test@email.com", "nom": "Test", "password": "1234"}
    ])
    def test_short_password(self,
                             test_client: Tuple[FlaskClient, Session],
                             payload: Dict) -> None:
        client, session = test_client
        client.post("/api/auth/register", json=payload)

        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 422
        assert resp.get_json()[0]["loc"] == ["password"]
        assert "at least 5 characters" in resp.get_json()[0]["msg"]

        user = session.query(User).filter_by(email=payload["email"]).one_or_none()
        assert user is None


    @pytest.mark.parametrize("payload", [
        {"email": "just@email.com"},
        {"nom": "justName", "password": "123456"}
    ])
    def test_missing_fields(self,
                            test_client: Tuple[FlaskClient, Session],
                            payload: Dict) -> None:
        """
        Vérifie l'échec de connexion si champ obligatoire manquant
        """
        client, session = test_client

        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 422
        assert "missing" in resp.get_json()[0]["type"]
        assert "email" or  "nom" or "password" in resp.get_json()[0]["loc"]
        assert "Field required" in resp.get_json()[0]["msg"]

        email = payload.get("email")
        if email:
            users = session.query(User).filter_by(email=email).all()
            assert len(users) == 0


class TestUserLogin:

    @pytest.mark.parametrize("payload", [
        {"email": "admin1@email.com", "nom": "Admin", "password": "admin", "role": "admin"},
        {"email": "client2@email.com", "nom": "Client", "password": "client"},
    ])
    def test_success(self, test_client: Tuple[FlaskClient, Session],
                     payload: Dict) -> None:
        client, session = test_client

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": payload["password"],
        })
        assert resp.status_code == 200

        data = resp.get_json()
        assert "token" in data

        token = data["token"]
        decoded = decode_token(token)
        assert decoded["email"] == payload["email"]

        email = payload.get("email")
        if email:
            user = session.query(User).filter_by(email=payload["email"]).one()
            assert decoded["role"] == user.role

    @pytest.mark.parametrize("wrong_password", ["pwd_nok", "123456"])
    def test_wrong_password(self,
                            test_client: Tuple[FlaskClient, Session],
                            wrong_password: str) -> None:
        client, _ = test_client
        payload = {
            "email": "login@email.com",
            "nom": "Wrong",
            "password": "pwd_ok"
        }

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": wrong_password
        })
        assert resp.status_code == 401

    @pytest.mark.parametrize("no_password", [None])
    def test_no_password(self,
                            test_client: Tuple[FlaskClient, Session],
                            no_password: None) -> None:
        client, _ = test_client
        payload = {
            "email": "login@email.com",
            "nom": "Wrong",
            "password": "pwd_ok"
        }

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": no_password
        })
        assert resp.status_code == 422
        assert resp.get_json()[0]["loc"] == ["password"]


class TestUserAccess:

    def test_access_ok(self, test_client: Tuple[FlaskClient, Session],
                       admin_token: str) -> None:
        client, session = test_client

        resp = client.get("/admin-route", headers={
        "Authorization": f"Bearer {admin_token}"
        })
        user = session.query(User).filter_by(role = "admin").first()

        assert user is not None
        assert resp.status_code == 200
        assert "Bienvenue" in resp.get_json()["message"]
        assert user.role == "admin"

    def test_access_denied(self,
                           test_client: Tuple[FlaskClient, Session],
                           client_token: str) -> None:
        client, _ = test_client

        resp = client.get("/admin-route", headers={
            "Authorization": f"Bearer {client_token}"
        })
        assert resp.status_code == 403
