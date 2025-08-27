from flask import request, jsonify, Blueprint
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from model.sessions import get_session
from core.utils import required_fields, register_user, login_user

auth_bp = Blueprint("auth", __name__)


# Routes :
@auth_bp.route('/register', methods=['POST'])
def register():
    '''
        Route pour l'inscription d'un utilisateur.
        Valide la présence des champs (obligatoires) du JSON reçu
        dans la requête et crée un utilisateur dans la Base de Données.

        Retourne un tuple:
            - dict: message de succès ou informations d'erreur
            - int: code HTTP (201, 400 ou 500)
    '''
    body = request.get_json()

    ok, error = required_fields(body, ["email", "nom", "password"])
    if not ok:
        return jsonify({"error": error}), 400

    session = get_session()

    try:
        new_user = register_user(
            session,
            email=body["email"],
            nom=body["nom"],
            password=body["password"],
            role=body.get("role", "client")
        )
        return jsonify(
            {"message": "User registered", "user": new_user.to_dict()}
            ), 201

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except IntegrityError:
        return jsonify({"error": "Duplicate email"}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to create user: {str(e)}"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    """
    Route pour l'authentification d'un utilisateur.
    Vérifie la présence des credentials du JSON reçu dans la requête,
    valide l'authentification de l'utilisateur et génère un token JWT.

    Retourne un tuple:
        - dict: message + token JWT ou informations d'erreur
        - int: code HTTP (200, 401 ou 500)
    """
    body = request.get_json()

    ok, error = required_fields(body, ["email", "password"])
    if not ok:
        return jsonify({"error": error}), 400

    session = get_session()

    try:
        token, _ = login_user(
            session,
            email=body["email"], password=body["password"]
            )
        return jsonify(
            {"message": "Connection succeed", "token": token}
            ), 200

    except ValueError as e:                         # Credentials non valides
        return jsonify({"error": str(e)}), 401
    except RuntimeError as e:                       # Token non généré
        return jsonify({"error": str(e)}), 500
    except SQLAlchemyError as e:
        return jsonify({"error": f"Failed to log in: {str(e)}"}), 500
