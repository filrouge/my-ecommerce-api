from flask import request, jsonify, Blueprint
from model.models import User
from core.auth import generate_token

from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from model.sessions import get_session


auth_bp = Blueprint("auth", __name__)


# Routes :
@auth_bp.route('/register', methods=['POST'])
def register():
    '''
        TODO: EXPLICATIONS
    '''
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400

    if not all(k in body for k in ("email", "nom", "password")):
        return jsonify({"error": "Missing fields"}), 400

    session = get_session()

    try:
        if session.query(User).filter_by(email=body["email"]).first():
            return jsonify({"error": "User already exists"}), 400

        new_user = User(
            email=body["email"],
            nom=body["nom"],
            password_hash=generate_password_hash(body["password"]),
            role=body.get("role", "client"),
            date_creation=datetime.now(UTC)
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)

        return jsonify(
            {"message": "User registered", "user": new_user.to_dict()}
            ), 201

    except IntegrityError:
        return jsonify({"error": "Duplicate email"}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    '''
        TODO: EXPLICATIONS
    '''
    body = request.get_json()
    if body is None:
        return jsonify({"error": "Invalid JSON"}), 400

    email = body.get("email")
    password = body.get("password")
    if not email or not password:
        return jsonify({"error": "Credentials required"}), 400

    session = get_session()

    try:
        user = session.query(User).filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        token = generate_token(user)
        if token is None:
            return jsonify({"error": "Token generation failed"}), 500

        return jsonify(
            {"message": "Connection succeed", "token": token}
            ), 200

    except IntegrityError:
        return jsonify({"error": "Duplicate email"}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500
