from pydantic import ConfigDict
from app.schemas.errors.validation_schemas import ValidationErrorsSchema


class RegisterError(ValidationErrorsSchema):
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

class LoginError(ValidationErrorsSchema):
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

class TokenError(ValidationErrorsSchema):
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