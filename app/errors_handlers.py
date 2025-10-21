from flask import Flask, jsonify
from sqlalchemy.exc import SQLAlchemyError
from app.core.exceptions.errors_maps import ORM_ERROR_MAP
from app.core.exceptions.app_errors import ApplicationError

from pydantic import ValidationError
from app.schemas.errors.json_schemas import (
    ValidationErrorItem, ValidationErrorSchema
)


def register_error_handlers(app: Flask) -> None:

    @app.errorhandler(ApplicationError)
    def handle_app_exceptions(error: ApplicationError):
        if isinstance(error, ApplicationError):
            return jsonify({"error": str(error)}), error.status_code

        return None

    @app.errorhandler(SQLAlchemyError)
    def handle_orm_exceptions(error: SQLAlchemyError):
        exc_name = error.__class__.__name__  # ex: "IntegrityError"
        if exc_name in ORM_ERROR_MAP:
            code, info = next(iter(ORM_ERROR_MAP[exc_name].items()))
            return jsonify({"error": info["error"]}), code

        # for exception_type, (code, msg) in ORM_ERROR_MAP.items():
        #     if isinstance(error, exception_type):
        #         # return jsonify({"error": f"Database - {msg}"}), code
        #         return jsonify({"error": msg}), code

        return jsonify({"error": "Database - Erreur interne inconnue"}), 500
    
    @app.errorhandler(ValidationError)
    def handle_validation_error(error: ValidationError):
        """ Formate en JSON les détails du ValidationError. """
        errors = [
            ValidationErrorItem(
                loc=err.get("loc", ()),
                msg=err.get("msg", ""),
                type=err.get("type", ""),
                # input=err.get("input"),
                # url=err.get("url")
            ) for err in error.errors()
        ]
        response = ValidationErrorSchema(errors=errors)
        return jsonify(response.model_dump()), 422
