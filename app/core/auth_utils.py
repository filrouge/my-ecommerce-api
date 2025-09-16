from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC, timedelta
from app.models import User
import jwt
from app.core.exceptions.app_errors import UnauthorizedError, BadRequestError
from sqlalchemy.orm import Session
from typing import Tuple
from flask import current_app


def jwt_settings() -> Tuple[str, str]:
    """Retourne un tuple des paramêtres JWT."""
    return (
        current_app.config.get("JWT_KEY"),
        current_app.config.get("ALGORITHM")
    )


# Générateur de token JWT
def generate_token(user: User) -> str:
    '''
    Génère un token JWT pour un utilisateur donné.
    Lève une erreur si la génération du token échoue.
    '''
    JWT_KEY, JWT_ALGO = jwt_settings()

    payload = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    token = jwt.encode(payload, JWT_KEY, JWT_ALGO)
    if not token:
        raise RuntimeError("La génération du token a échoué")

    return token


def decode_token(token: str) -> dict:
    """Décode un JWT et lève UnauthorizedError si invalide ou expiré."""
    JWT_KEY, JWT_ALGO = jwt_settings()

    try:
        payload = jwt.decode(token, JWT_KEY, JWT_ALGO)
        return payload
    except jwt.ExpiredSignatureError:
        raise UnauthorizedError("Token expiré")
    except jwt.InvalidTokenError:
        raise UnauthorizedError("Token invalide")


def get_user_by_email(session: Session, email: str) -> User | None:
    '''
    Récupère une instance d'utilisateur par son email (None si inexistant).
    '''
    return session.query(User).filter_by(email=email).first()


def register_user(session: Session, email: str,
                  nom: str, password: str, role: str) -> User:
    '''
    Crée un nouvel utilisateur dans la base et
    retourne l'instance de l'utilisateur créé.

    Lève une erreur si l'email est déjà utilisé.
    '''
    if get_user_by_email(session, email):
        raise BadRequestError("Adresse e-mail déjà utilisée")

    user = User(
        email=email,
        nom=nom,
        password_hash=generate_password_hash(password),
        role=role,
        date_creation=datetime.now(UTC),
    )
    session.add(user)
    # session.flush()
    session.commit()
    session.refresh(user)

    return user


def login_user(session: Session, email: str,
               password: str) -> Tuple[str, User]:
    '''
    Vérifie les identifiants utilisateur et génère un token JWT.

    Retourne le token généré avec l'instance utilisateur associée.
    Lève une erreur si identifiants invalides.
    '''
    user = get_user_by_email(session, email)
    if not user or not check_password_hash(user.password_hash, password):
        raise UnauthorizedError("Identifiants invalides")

    token = generate_token(user)
    return token, user
