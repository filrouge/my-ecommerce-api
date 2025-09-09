from flask import request, g
import jwt
from functools import wraps
from app.model.models import User
from app.core.exceptions.app_errors import UnauthorizedError, ForbiddenError
from typing import Callable, Any

from app.core.auth_utils import decode_token

# Décorateur Authentification (token JWT)
def auth_required(func: Callable) -> Callable:
    '''
    Vérifie la présence et la validité du token
    dans l'en-tête `Authorization: Bearer <token>`.
    Utilise g.session pour les requêtes SQLAlchemy.

    Retourne une fonction décorée appliquant la vérification JWT.
    Lève une erreur si token expiré, invalide ou manquant.
    '''
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise UnauthorizedError("Token manquant")

        token = auth_header.split(" ")[1]
        payload = decode_token(token)
        user_id = payload.get("id")
        if not user_id:
            raise UnauthorizedError("Payload Token invalide")

        session = g.session
        try:
            user = session.get(User, user_id)
            if not user:
                raise UnauthorizedError("Utilisateur introuvable")

            g.current_user = user

            return func(current_user=user, *args, **kwargs)
        finally:
            session.close()

    return wrapper


# Décorateur Autorisation (rôle) :
def access_granted(*role_names: str) -> Callable:
    """
    Vérifie le(s) rôle(s) pour autoriser des actions CRUD
    (@access_granted(role) avec role = "client" et/ou "admin")
    
    Retourne une fonction décorée appliquant la vérification du rôle.
    Lève une erreur si (rôle) utilisateur non autorisé
    """
    def decorator(func: Callable) -> Callable:
        @auth_required
        @wraps(func)
        def wrapper(current_user=None, *args, **kwargs):
            if current_user is None:
                raise UnauthorizedError("Utilisateur non reconnu")

            if role_names and current_user.role not in role_names:
                raise ForbiddenError("Accès refusé")

            return func(*args, **kwargs)
        return wrapper
    return decorator
