from flask import Flask, request, jsonify
from models import User
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)

# JWT secret:
# (TODO: env_var in config/env file)
JWT_KEY = "secret"
ALGORITHM = "HS256"

table_users = []


# JWT Token Generator
def generate_token(user):
    payload = {
        # "id": user.id,
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


# Routes :
@app.route("/")
def index():
    return "e-commerce API is operating"


@app.route('/api/auth/register', methods=['POST'])
def register():
    global table_users
    body = request.json

    if not all(k in body for k in ("email", "nom", "password", "role")):
        return jsonify({"error": "Missing fields"}), 400

    if any(u.email == body["email"] for u in table_users):
        return jsonify({"error": "User already exists"}), 400

    try:
        new_user = User(email=body["email"],
                        nom=body["nom"],
                        password=body["password"],
                        role=body["role"]
                        )
        table_users.append(new_user)

    except Exception as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

    return jsonify({"message": "User registered",
                    "user": new_user.to_dict()
                    }), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    body = request.json
    email = body.get("email")
    password = body.get("password")

    if not email or not password:
        return jsonify({"error": "Credentials required"}), 400

    user = next((u for u in table_users if u.email == email), None)
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = generate_token(user)
    if token is None:
        return jsonify({"error": "Token generation failed"}), 500

    return jsonify({"message": "Connection succeed", "token": token})


# Following is for tests and check purposes
@app.route("/api/admin-space/users", methods=["GET"])
def list_users():
    # import pdb
    # pdb.set_trace()  #breakpoint
    try:
        users_list = [user.to_dict() for user in table_users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": f"Serialization Error : {str(e)}"}), 500


@app.route("/api/admin-route")
@auth_required
def admin_route(current_user):
    if current_user.get("role") != "admin":
        return jsonify({"error": "Access forbidden"}), 403
    else:
        return jsonify({"message": f"Welcome {current_user.get('email')} !"})
