from flask import jsonify
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


# Classes des exceptions applicatives customisées
class ApplicationError(Exception):
    """Exception générique pour toutes les erreurs applicatives."""
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.status_code = status_code


class BadRequestError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=400)


class UnauthorizedError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=401)


class ForbiddenError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=403)


class NotFoundError(ApplicationError):
    def __init__(self, message):
        super().__init__(message, status_code=404)


def register_error_handlers(app):
    # Handler pour les erreurs applicatives
    @app.errorhandler(ApplicationError)
    def handle_app_exceptions(error):
        if isinstance(error, ApplicationError):
            return jsonify({"error": str(error)}), error.status_code

        return None

    @app.errorhandler(SQLAlchemyError)
    def handle_orm_exceptions(error):
        # # Pour DEBUG seulement -- centraliser condition PROD/DEV ?
        # if isinstance(error, IntegrityError):
        #     return jsonify({
        #         "error": f"Database - Contrainte d'intégrité violée \
        #             ({error.orig})"
        #         }), 409

        for exception_type, (code, msg) in ORM_ERROR_MAP.items():
            if isinstance(error, exception_type):
                # return jsonify({"error": f"Database - {msg}"}), code
                return jsonify({"error": msg}), code

        return jsonify({"error": "Database - Erreur interne inconnue"}), 500
