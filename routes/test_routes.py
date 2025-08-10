from flask import jsonify, Blueprint
from core.auth import table_users
from core.auth import auth_required


test_bp = Blueprint("api", __name__)


# Following routes are for tests and check purposes
@test_bp.route("/admin-space/users", methods=["GET"])
def list_users():
    # import pdb
    # pdb.set_trace()  #breakpoint
    try:
        users_list = [user.to_dict() for user in table_users]
        return jsonify(users_list)
    except Exception as e:
        return jsonify({"error": f"Serialization Error : {str(e)}"}), 500


@test_bp.route("/admin-route")
@auth_required
def admin_route(current_user):
    if current_user.get("role") != "admin":
        return jsonify({"error": "Access forbidden"}), 403
    else:
        return jsonify({"message": f"Welcome {current_user.get('email')} !"})
