from flask import request, jsonify, g
import jwt
from functools import wraps
from model.models import User
from model.sessions import get_session
from config import Config


# JWT secret
JWT_KEY = Config.JWT_KEY
ALGORITHM = "HS256"


# Authentification
def auth_required(func):
    '''
    Décorateur pour authentification via token JWT qui en vérifie
    la validité dans l'en-tête `Authorization: Bearer <token>`.
    Retourne une fonction décorée appliquant la vérification JWT.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token manquant"}), 401

        token = auth_header.split(" ")[1]
        try:
            current_user = jwt.decode(token, JWT_KEY, algorithms=[ALGORITHM])
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expiré"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Token invalide"}), 401

        user_id = current_user.get("id")
        if not user_id:
            return jsonify({"error": "Payload Token invalide"}), 401

        session = get_session()
        try:
            user = session.get(User, user_id)
            if not user:
                return jsonify({"error": "Utilisateur introuvable"}), 401

            # Ajouter g.current_user: absent -> echec sur "commandes" !
            g.current_user = user

            return func(current_user=user, *args, **kwargs)
        finally:
            session.close()

    return wrapper


# Autorisation
def access_granted(*role_names):
    """
    Décorateur autorisant les actions CRUD selon le role :
        @access_granted("admin")
        @access_granted("client", "admin")
    """
    def decorator(func):
        @auth_required
        @wraps(func)
        def wrapper(current_user=None, *args, **kwargs):
            # current_user = kwargs.pop("current_user")
            if current_user is None:    # Optionnel/Redondant
                return jsonify({"error": "Utilisateur non reconnu"}), 401

            if role_names and current_user.role not in role_names:
                return jsonify({"error": "Accès refusé"}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator
