from flask import request, jsonify, Blueprint
from model.models import User
from core.auth import table_users
from core.auth import generate_token


auth_bp = Blueprint("auth", __name__)


# Routes :
@auth_bp.route('/register', methods=['POST'])
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


@auth_bp.route("/login", methods=["POST"])
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
