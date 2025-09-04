'''
    Point d'entrée pour la création de session SQLAlchemy
    avec gestion centralisée 'flask.g'
'''

from flask import g
from model.database import SessionLocal


def get_session():
    """ Renvoie une session SQLAlchemy stockée dans g. """
    if "session" not in g:
        g.session = SessionLocal()
    return g.session


def close_session():
    """ Cloture automatique de la session après chaque requête. """
    session = g.pop("session", None)
    if session:
        session.close()


def init_session(app):
    """
    Initialise les hooks Flask pour la session
    avec rollback automatique si exception :
        - création de la session avant chaque requête
        - fermeture de la session après chaque requête
        - factorisation des erreurs/exceptions ORM
    """

    @app.before_request
    def before_request():
        """ Création de la session. """
        get_session()

    @app.teardown_appcontext
    def teardown_session(exception=None):
        ''' Fermeture de la session '''
        session = g.get("session", None)
        if exception and session:
            session.rollback()
        close_session()
