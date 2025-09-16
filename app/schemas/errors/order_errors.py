from pydantic import ConfigDict
from app.schemas.errors.validation_schemas import ValidationErrorsSchema

# Erreurs dédiées par endpoint - classes (avec example via json_schema_extra)
class OrderCreateError(ValidationErrorsSchema):
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

class OrderUpdateError(ValidationErrorsSchema):
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

class OrderDeleteError(ValidationErrorsSchema):
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

class OrderListError(ValidationErrorsSchema):
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

class OrderGetError(ValidationErrorsSchema):
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
