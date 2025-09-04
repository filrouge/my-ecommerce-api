from flask import Blueprint, jsonify, g
from core.auth import auth_required
from model.models import User
from model.sessions import get_session

main_bp = Blueprint("main", __name__)


# Routes :
@main_bp.route("/")
def home():
    return "API e-commerce opérationnelle !"


# Routes pour test et checks manuels
@main_bp.route("/admin-space/users", methods=["GET"])
@auth_required
def list_users(current_user):
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
def public_list_users():
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
def admin_route(current_user):
    if current_user.role != "admin":
        return jsonify({"error": "Accès refusé"}), 403
    else:
        return jsonify({"message": f"Bienvenue {current_user.email} !"})
