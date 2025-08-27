import jwt
from datetime import datetime
from werkzeug.security import check_password_hash
from model.models import User
from config import Config
from core.utils import get_user_by_email


class TestRegister:

    def test_new_user(self, test_client):
        client, session = test_client
        payload = {
            "email": "test@email.com",
            "nom": "Test",
            "password": "123456"
        }
        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 201

        data = resp.get_json()
        assert data["message"] == "User registered"
        assert data["user"]["email"] == payload["email"]
        assert data["user"]["role"] == "client"

        # user = session.query(User).filter_by(email=payload["email"]).first()
        user = get_user_by_email(session, payload["email"])
        assert check_password_hash(user.password_hash, payload["password"])
        assert isinstance(user.date_creation, datetime)

    def test_duplicate_email(self, test_client):
        client, session = test_client
        payload = {
            "email": "duplicated@email.com",
            "nom": "Duplicate",
            "password": "123456"
        }
        # Inscription / Ré-inscription avec email identique
        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 400
        assert resp.get_json()["error"] == "User already exists"

        # Vérification au niveau BdD
        users = session.query(User).filter_by(email=payload["email"]).all()
        assert len(users) == 1

    def test_missing_fields(self, test_client):
        client, session = test_client
        payload = {
            "email": "just@email.com"
        }
        resp = client.post("/api/auth/register", json=payload)
        assert resp.status_code == 400
        assert "missing" in resp.get_json()["error"].lower()

        users = session.query(User).filter_by(email=payload["email"]).all()
        assert len(users) == 0


class TestLogin:

    def test_success(self, test_client):
        client, _ = test_client
        payload = {
            "email": "admin@email.com",
            "nom": "Admin",
            "password": "admin",
            "role": "admin"
        }
        JWT_KEY = Config.JWT_KEY
        ALGORITHM = "HS256"

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": payload["password"]
        })
        assert resp.status_code == 200
        data = resp.get_json()
        assert "token" in data

        token = data["token"]
        decoded = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        assert decoded["email"] == payload["email"]
        assert decoded["role"] == payload["role"]

    def test_wrong_password(self, test_client):
        client, _ = test_client
        payload = {
            "email": "login@email.com",
            "nom": "Wrong",
            "password": "pwd_ok"
        }

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": "pwd_nok"
        })
        assert resp.status_code == 401


class TestAdminAccess:
    def test_access_ok(self, test_client):
        client, session = test_client
        payload = {
            "email": "super_admin@email.com",
            "nom": "Super_Admin",
            "password": "admin",
            "role": "admin"
        }

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": payload["password"]
        })

        token = resp.get_json()["token"]
        resp = client.get("/api/admin-route", headers={
            "Authorization": f"Bearer {token}"
        })
        # user = session.query(User).filter_by(email=payload["email"]).first()
        user = get_user_by_email(session, payload["email"])

        assert resp.status_code == 200
        assert "Welcome" in resp.get_json()["message"]
        assert user.role == payload["role"]

    def test_access_denied(self, test_client):
        client, _ = test_client
        payload = {
            "email": "not_admin@email.com",
            "nom": "Client",
            "password": "123456",
            "role": "client"
        }

        client.post("/api/auth/register", json=payload)
        resp = client.post("/api/auth/login", json={
            "email": payload["email"],
            "password": payload["password"]
        })

        token = resp.get_json()["token"]
        resp = client.get("/api/admin-route", headers={
            "Authorization": f"Bearer {token}"
        })
        assert resp.status_code == 403
