from flask import jsonify, Blueprint
from core.auth import auth_required

from model.models import User
from core.auth import SessionLocal

test_bp = Blueprint("api", __name__)


# Following routes are for tests and check purposes
@test_bp.route("/admin-space/users", methods=["GET"])
@auth_required
def list_users(current_user):
    if current_user.role != "admin":
        return jsonify({"error": "Unauthorized"}), 403

    session = SessionLocal()
    try:
        users = session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": f"Serialization Error : {str(e)}"}), 500
    finally:
        session.close()


@test_bp.route("/public-space/users", methods=["GET"])
def public_list_users():
    session = SessionLocal()
    try:
        users = session.query(User).all()
        return jsonify([u.to_dict() for u in users])
    except Exception as e:
        return jsonify({"error": f"Serialization Error : {str(e)}"}), 500
    finally:
        session.close()


# @test_bp.route("/admin-route")
# @auth_required
# def admin_route(current_user):
#     if current_user.role != "admin":
#         return jsonify({"error": "Access forbidden"}), 403
#     else:
#         return jsonify({"message": f"Welcome {current_user.email} !"})
