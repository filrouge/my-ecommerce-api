from flask import jsonify, Blueprint
from core.auth import auth_required

from model.models import User
from model.sessions import get_session

test_bp = Blueprint("api", __name__)


# Routes pour test et checks manuels
@test_bp.route("/admin-space/users", methods=["GET"])
@auth_required
def list_users(current_user):
    '''
        TODO: EXPLICATIONS
    '''
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    session = get_session()
    try:
        users = session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": f"Serialization Error : {str(e)}"}), 500


@test_bp.route("/public-space/users", methods=["GET"])
def public_list_users():
    '''
        TODO: EXPLICATIONS
    '''
    session = get_session()
    try:
        users = session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": f"Serialization Error : {str(e)}"}), 500


@test_bp.route("/admin-route")
@auth_required
def admin_route(current_user):
    if current_user.role != "admin":
        return jsonify({"error": "Access forbidden"}), 403
    else:
        return jsonify({"message": f"Welcome {current_user.email} !"})
