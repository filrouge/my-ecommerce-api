from pydantic import ConfigDict
from app.schemas.errors.json_schemas import ValidationErrorSchema
from app.schemas.errors.errors_schemas import ErrorClass

"""
    Erreurs dédiées par endpoint - classes (exemple via json_schema_extra)
"""

# REGISTER
class RegisterError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ["nom", "email"],
                        "msg": "Field required",
                        "type": "missing"
                    }
                ]
            }
        }
    )

# LOGIN
class LoginError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ["password", "email"],
                        "msg": "Email ou mot de passe invalide",
                        "type": "missing"
                    }
                ]
            }
        }
    )

# TOKEN
class TokenError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ["email"],
                        "msg": "Identifiants invalides",
                        "type": "auth_error"
                    }
                ]
            }
        }
    )


UserError400 = ErrorClass("user", 400)
UserError401 = ErrorClass("user", 401)
UserError403 = ErrorClass("user", 403)
UserError404 = ErrorClass("user", 404)