from flask import request, jsonify, Blueprint, g, Response
from app.core.auth_utils import register_user, login_user, check_credentials_strength
from app.services.validators import (
    get_json_body, validate_json_fields,
    USER_FIELDS
    )
from typing import Tuple

auth_bp = Blueprint("auth", __name__)


# POST /api/auth/register
@auth_bp.route('/register', methods=['POST'])
def register() -> Tuple[Response, int]:
    '''
        Route pour l'inscription d'un utilisateur.
        Valide la présence des champs (obligatoires) du JSON reçu
        dans la requête et crée un utilisateur dans la Base de Données.

        Retourne un tuple:
            - dict: message de succès ou informations d'erreur
            - int: code HTTP (201, 400 ou 500)
    '''
    body = get_json_body(request)
    validate_json_fields(body, USER_FIELDS, {"role"})
    check_credentials_strength(body)

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


# POST /api/auth/login
@auth_bp.route("/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Route pour l'authentification d'un utilisateur.
    Vérifie la présence des credentials du JSON reçu dans la requête,
    valide l'authentification de l'utilisateur et génère un token JWT.

    Retourne un tuple:
        - dict: message + token JWT ou informations d'erreur
        - int: code HTTP (200, 401 ou 500)
    """
    body = get_json_body(request)
    validate_json_fields(body, USER_FIELDS, {"nom", "role"})

    token, _ = login_user(
        g.session,
        email=body["email"], password=body["password"]
        )
    return jsonify(
        {"message": "Connexion réussie", "token": token}
        ), 200
