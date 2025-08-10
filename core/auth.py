from flask import request, jsonify
import jwt
from functools import wraps
from datetime import datetime, timedelta


# JWT secret:
# (TODO: env_var in config/env file)
JWT_KEY = "secret"
ALGORITHM = "HS256"

table_users = []


# JWT Token Generator
def generate_token(user):
    payload = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }
    try:
        token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
        return token
    except Exception as e:
        print(f"JWT generation failed: {e}")
        return None


def auth_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            current_user = jwt.decode(token, JWT_KEY, algorithms=ALGORITHM)
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return func(current_user=current_user, *args, **kwargs)

    return wrapper
