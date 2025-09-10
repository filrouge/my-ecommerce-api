from flask import g, Flask
from app.database.base import SessionLocal
from sqlalchemy.orm import Session
from typing import Optional

'''
initialisation de session avec gestion centralisée 'flask.g'
'''


def get_session() -> Session:
    """ Renvoie une session SQLAlchemy stockée dans g. """
    if "session" not in g:
        g.session = SessionLocal()
    return g.session


def close_session() -> None:
    """ Cloture automatique de la session après chaque requête. """
    session = g.pop("session", None)
    if session:
        session.close()


def init_session(app: Flask) -> None:
    """
    Initialise les hooks Flask pour la session
    avec rollback automatique si exception :
        - création de la session avant chaque requête
        - fermeture de la session après chaque requête
        - factorisation des erreurs/exceptions ORM
    """

    @app.before_request
    def before_request() -> None:
        """ Création de la session. """
        get_session()

    @app.teardown_appcontext
    def teardown_session(exception: Optional[BaseException] = None) -> None:
        ''' Fermeture de la session '''
        session = g.get("session", None)
        if exception and session:
            session.rollback()
        close_session()
