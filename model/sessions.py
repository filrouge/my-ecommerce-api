'''
    Point d'entrée pour la création de session SQLAlchemy
    avec gestion centralisée 'flask.g' des sessions
'''

from flask import g
from model.database import SessionLocal


# Getting the unique request session
def get_session():
    """
        Return SQLAlchemy session stored
        and integrated into g.
    """
    if "session" not in g:
        g.session = SessionLocal()
    return g.session


# Close the unique request session
def close_session():
    """
        Close the g session automatically
        after the end of each request.
    """
    session = g.pop("session", None)
    if session:
        session.close()


def init_session(app):
    """
    Initialise les hooks Flask pour la session par
    requête avec rollback automatique si exception :
        - avant chaque requête : création de la session
        - après chaque requête : fermeture de la session
    """

    # Création de la session
    @app.before_request
    def before_request():
        get_session()

    # Fermeture de la session
    @app.teardown_appcontext
    def teardown_session(exception=None):
        session = g.get("session", None)
        if exception and session:
            session.rollback()
        close_session()
