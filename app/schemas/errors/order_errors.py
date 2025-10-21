from pydantic import ConfigDict
from app.schemas.errors.json_schemas import ValidationErrorSchema
from app.schemas.errors.errors_schemas import ErrorClass

# Erreurs dédiées par endpoint - classes (exemple via json_schema_extra)
class OrderCreateError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("produits", 0, "quantite"),
                        "msg": "Quantité doit être >= 0",
                        "type": "value_error.number.not_ge",
                        "input": "-1",
                        "url": None
                    }
                ]
            }
        }
    )

class OrderUpdateError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("lignes",),
                        "msg": "Liste de produits ne doit pas être vide",
                        "type": "value_error.list.min_items",
                        "input": [],
                        "url": None
                    }
                ]
            }
        }
    )

class OrderDeleteError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("order_id",),
                        "msg": "Commande introuvable",
                        "type": "not_found",
                        "input": "999",
                        "url": None
                    }
                ]
            }
        }
    )

class OrderListError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("limit",),
                        "msg": "Limit doit être un entier positif",
                        "type": "value_error.number.not_ge",
                        "input": "-1",
                        "url": None
                    }
                ]
            }
        }
    )

class OrderGetError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("order_id",),
                        "msg": "Commande introuvable ou accès refusé",
                        "type": "not_found",
                        "input": "999",
                        "url": None
                    }
                ]
            }
        }
    )


OrderError400 = ErrorClass("order", 400)
OrderError401 = ErrorClass("order", 401)
OrderError403 = ErrorClass("order", 403)
OrderError404 = ErrorClass("order", 404)