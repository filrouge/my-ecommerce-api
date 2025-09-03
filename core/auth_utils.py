from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, UTC, timedelta
from model.models import User
import jwt
from config import Config


# JWT secret
JWT_KEY = Config.JWT_KEY
ALGORITHM = "HS256"


def required_fields(data, required):
    '''
    Vérifie et valide la présence des champs requis.
    Retourne un tuple (ok, message_erreur).
    '''
    if not data:
        return False, "JSON invalide"

    missing = [field for field in required if field not in data]
    if missing:
        return False, f"Champs manquant(s) : {', '.join(missing)}"

    return True, None


# def required_fields(data, required):
#     '''
#     Vérifie et valide la présence des champs requis.
#     Retourne un tuple (ok, message_erreur).
#     '''
    # if not data:
    #     raise ValueError("JSON invalide")

    # missing = [field for field in required if field not in data]
    # if missing:
    #     raise ValueError(f"Champs manquant(s) : {', '.join(missing)}")


# Générateur de token JWT
def generate_token(user):
    '''
    Génère un token JWT pour une instance d'utilisateur donné (user).
    Retourne le token JWT encodé si la génération réussit, sinon `None`.
    '''
    payload = {
        "id": user.id,
        "email": user.email,
        "role": user.role,
        "exp": datetime.now(UTC) + timedelta(hours=1)
    }
    try:
        token = jwt.encode(payload, JWT_KEY, algorithm=ALGORITHM)
        return token

    except Exception:
        return None


def get_user_by_email(session, email):
    '''Retourne un utilisateur par son email, ou None si inexistant.'''
    return session.query(User).filter_by(email=email).first()


def register_user(session, email, nom, password, role):
    '''Enregistre un utilisateur dans la Base de Données.'''
    if get_user_by_email(session, email):
        raise ValueError("Adresse e-mail déjà utilisée")

    user = User(
        email=email,
        nom=nom,
        password_hash=generate_password_hash(password),
        role=role,
        date_creation=datetime.now(UTC),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def login_user(session, email, password):
    '''Vérifie les credentials utilisateur et génère un token JWT.'''
    user = get_user_by_email(session, email)
    if not user or not check_password_hash(user.password_hash, password):
        raise ValueError("Identifiants invalides")

    token = generate_token(user)
    if not token:
        raise RuntimeError("La génération du token a échoué")

    return token, user
