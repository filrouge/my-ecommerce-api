'''
    Point d'entrée pour la création de session SQLAlchemy
    avec gestion centralisée 'flask.g'
'''

from flask import g, jsonify
from model.database import SessionLocal
from sqlalchemy.exc import (
    SQLAlchemyError,
    IntegrityError,
    OperationalError,
    DataError,
    StatementError
)

# Mapping des exceptions ORM
ORM_ERROR_MAP = {
    IntegrityError: (409, "Contrainte d'intégrité violée"),
    OperationalError: (503, "Service database indisponible"),
    DataError: (400, "Donnée invalide ou contrainte violée"),
    StatementError: (500, "Erreur dans la requête SQL"),
}


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

    @app.errorhandler(SQLAlchemyError)
    def handle_orm_exceptions(error):
        # Pour DEBUG seulement -- condition à centraliser ?
        # if isinstance(error, IntegrityError):
        #     return jsonify(
        #         {"error": f"Contrainte d'intégrité violée -  {error.orig}"}
        #         ), 409

        for exception_type, (code, msg) in ORM_ERROR_MAP.items():
            if isinstance(error, exception_type):
                return jsonify({"error": msg}), code

        return jsonify({"error": "Erreur interne de la database"}), 500
