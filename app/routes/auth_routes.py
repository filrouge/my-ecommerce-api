from flask import request, jsonify, Blueprint, g, Response
from app.core.auth_utils import register_user, login_user
from typing import Tuple

from app.schemas.auth_schemas import RegisterSchema, LoginSchema, UserRespSchema, TokenRespSchema, RegisterRespSchema
from pydantic import ValidationError
from app.schemas.errors.auth_errors import RegisterError, LoginError, TokenError
from spectree import Response as SpecResp
from app.spec import spec

auth_bp = Blueprint("auth", __name__)


# POST /api/auth/register
@auth_bp.route('/register', methods=['POST'])
@spec.validate(json=RegisterSchema, resp=SpecResp(HTTP_201=RegisterRespSchema, HTTP_422=RegisterError), tags=["Users"])
def register() -> Tuple[Response, int]:
    '''
        Route pour l'inscription d'un utilisateur.
        Valide le JSON de la requête et crée un utilisateur.

        Retourne un tuple:
            - dict: message de succès ou informations d'erreur
            - int: code HTTP (201, 400 ou 500)
    '''
    try:
        body = RegisterSchema(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422
    
    body = body.model_dump()
    new_user = register_user(
        g.session,
        email=body["email"],
        nom=body["nom"],
        password=body["password"],
        role=body.get("role", "client")
    )
    response = UserRespSchema.model_validate(new_user)
    # response = RegisterRespSchema(message = "Client inscrit", user=UserRespSchema.model_validate(new_user))
    return jsonify({"message": "Client inscrit", "user": response.model_dump()}), 201
    # return jsonify(response.model_dump()), 201


# POST /api/auth/login
@auth_bp.route("/login", methods=["POST"])
@spec.validate(json=LoginSchema, resp=SpecResp(HTTP_200=TokenRespSchema, HTTP_422=LoginError, HTTP_401=TokenError), tags=["Users"])
def login() -> Tuple[Response, int]:
    """
    Route pour l'authentification d'un utilisateur.
    Vérifie et valide l'authentification de l'utilisateur et génère un token JWT.

    Retourne un tuple:
        - dict: message + token JWT ou informations d'erreur
        - int: code HTTP (200, 401 ou 500)
    """
    try:
        body = LoginSchema(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    body = body.model_dump()

    token, _ = login_user(
        g.session,
        email=body["email"], password=body["password"]
        )
    response = TokenRespSchema(token=token, message="Connexion réussie")
    return jsonify(response.model_dump()), 200
