from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from .exceptions.orm_errors import ORM_ERROR_MAP
from .exceptions.app_errors import ApplicationError


def register_error_handlers(app: Flask) -> None:
    # Handler pour les erreurs applicatives
    @app.errorhandler(ApplicationError)
    def handle_app_exceptions(error: ApplicationError):
        if isinstance(error, ApplicationError):
            return jsonify({"error": str(error)}), error.status_code

        return None

    @app.errorhandler(SQLAlchemyError)
    def handle_orm_exceptions(error: SQLAlchemyError):
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
