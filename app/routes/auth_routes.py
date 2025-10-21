from flask import request, jsonify, Blueprint, g, Response
from app.core.auth_utils import register_user, login_user
from typing import Tuple

from app.schemas.user_schemas import (
    RegisterSchema, LoginSchema, UserRespSchema, TokenRespSchema, RegisterRespSchema
)
from app.schemas.errors.user_errors import (
    RegisterError, LoginError,
    UserError400, UserError401, UserError403, UserError404
)
from spectree import Response as SpecResp
from app.spec import spec

auth_bp = Blueprint("auth", __name__)


# POST /api/auth/register
@auth_bp.route('/register', methods=['POST'])
@spec.validate(
    json=RegisterSchema,
    resp=SpecResp(HTTP_201=RegisterRespSchema, HTTP_422=RegisterError,
                  HTTP_400=UserError400, HTTP_401=UserError401,
                  HTTP_403=UserError403,HTTP_404=UserError404),
    tags=["Users"]
)
def register() -> Tuple[Response, int]:
    '''
        Inscription utilisateur.
    '''
    body = request.json

    new_user = register_user(
        g.session,
        email=body["email"],
        nom=body["nom"],
        password=body["password"],
        role=body.get("role", "client")
    )
    response = UserRespSchema.model_validate(new_user)
    return jsonify({"message": "Client inscrit", "user": response.model_dump()}), 201


# POST /api/auth/login
@auth_bp.route("/login", methods=["POST"])
@spec.validate(
    json=LoginSchema,
    resp=SpecResp(HTTP_200=TokenRespSchema, HTTP_422=LoginError,
                  HTTP_400=UserError400, HTTP_401=UserError401,
                  HTTP_403=UserError403,HTTP_404=UserError404),
    tags=["Users"]
)
def login() -> Tuple[Response, int]:
    """
    Authentification utilisateur.
    """
    body = request.json

    token, _ = login_user(
        g.session,
        email=body["email"], password=body["password"]
        )
    response = TokenRespSchema(token=token, message="Connexion réussie")
    return jsonify(response.model_dump()), 200
