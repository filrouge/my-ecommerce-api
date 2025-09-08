from flask import Blueprint, jsonify, g, Response
from app.core.auth import auth_required
from app.model.models import User
from app.model.sessions import get_session
from typing import Tuple

main_bp = Blueprint("main", __name__)


# Routes :
@main_bp.route("/")
def home() -> str:
    return "API e-commerce opérationnelle !"


# Routes pour test et checks manuels
@main_bp.route("/admin-space/users", methods=["GET"])
@auth_required
def list_users(current_user: User) -> Tuple[Response, int] | Response:
    '''
        TODO: EXPLICATIONS
    '''
    if current_user.role != "admin":
        return jsonify({"error": "Accès refusé"}), 403

    session = get_session()
    try:
        users = session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": f"Erreur de sérialisation : {str(e)}"}), 500


@main_bp.route("/public-space/users", methods=["GET"])
def public_list_users() -> Tuple[Response, int] | Response:
    '''
        TODO: EXPLICATIONS
    '''
    try:
        users = g.session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": f"Erreur de sérialisation : {str(e)}"}), 500


@main_bp.route("/admin-route")
@auth_required
def admin_route(current_user: User) -> Tuple[Response, int] | Response:
    if current_user.role != "admin":
        return jsonify({"error": "Accès refusé"}), 403
    else:
        return jsonify({"message": f"Bienvenue {current_user.email} !"})
