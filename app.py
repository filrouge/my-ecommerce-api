from flask import Flask, request, jsonify
from models import User

app = Flask(__name__)

# JWT secret:
# (TODO: env_var in config/env file)
JWT_KEY = "secret"
ALGORITHM = "HS256"

table_users = []


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
        # hashed_password = generate_password_hash(body["password"])
        new_user = User(email=body["email"], nom=body["nom"],
                        password=body["password"], role=body["role"]
                        )
        table_users.append(new_user)

    except Exception as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500

    return jsonify({"message": "User registered",
                    "user": new_user.to_dict()
                    }), 201


'''
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
'''
