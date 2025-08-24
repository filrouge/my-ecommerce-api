from flask import request, jsonify
import jwt
from functools import wraps
from datetime import datetime, UTC, timedelta

from model.models import User
# from model.database import SessionLocal
from model.sessions import get_session
from config import Config


# JWT secret
JWT_KEY = Config.JWT_KEY
ALGORITHM = "HS256"


# Générateur de token JWT
def generate_token(user):
    payload = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    try:
        token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        print(f"JWT generation failed: {e}")
        return None


# Authentification
def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            current_user = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        user_id = current_user.get("id")
        if not user_id:
            return jsonify({"error": "Invalid token payload"}), 401

        session = get_session()
        try:
            user = session.get(User, user_id)
            if not user:
                return jsonify({"error": "User not found"}), 401
            return func(current_user=user, *args, **kwargs)
        finally:
            session.close()

    return wrapper
