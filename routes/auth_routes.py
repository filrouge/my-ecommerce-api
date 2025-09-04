from flask import request, jsonify, Blueprint, g
# from model.sessions import get_session
from core.auth_utils import register_user, login_user
from core.request_utils import (
    get_json_body,
    required_fields,
    REGISTER_FIELDS
    )

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
    body = get_json_body(request)
    required_fields(body, REGISTER_FIELDS)

    new_user = register_user(
        g.session,
        email=body["email"],
        nom=body["nom"],
        password=body["password"],
        role=body.get("role", "client")
    )
    return jsonify(
        {"message": "Client inscrit", "user": new_user.to_dict()}
        ), 201


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
    body = get_json_body(request)

    LOGIN_FIELDS = REGISTER_FIELDS.copy()
    LOGIN_FIELDS.pop("nom", None)
    required_fields(body, LOGIN_FIELDS)

    # session = get_session()

    token, _ = login_user(
        g.session,
        email=body["email"], password=body["password"]
        )
    return jsonify(
        {"message": "Connexion réussie", "token": token}
        ), 200
