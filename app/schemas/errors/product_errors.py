from app.schemas.errors.json_schemas import ValidationErrorSchema
from pydantic import ConfigDict
from app.schemas.errors.errors_schemas import ErrorClass

"""
    Erreurs dédiées par endpoint - classes (exemple via json_schema_extra)
"""

# CREATE
class ProductCreateError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("prix",),
                        "msg": "Input should be a valid number",
                        "type": "float_parsing",
                        # "input": "str",
                        # "url": "https://errors.pydantic.dev/2.11/v/float_parsing"
                    }
                ]
            }
        }
    )

# UPDATE
class ProductUpdateError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("quantite_stock",),
                        "msg": "Value must be greater than or equal to 0",
                        "type": "value_error.number.not_ge",
                    #     "input": "-5",
                    #     "url": "https://errors.pydantic.dev/2.11/v/value_error.number.not_ge"
                    }
                ]
            }
        }
    )

# DELETE
class ProductDeleteError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("product_id",),
                        "msg": "Produit non trouvé",
                        "type": "not_found",
                        # "input": "999",
                        # "url": None
                    }
                ]
            }
        }
    )

# LIST
class ProductListError(ValidationErrorSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("limit",),
                        "msg": "Paramètre doit être un entier positif",
                        "type": "value_error.number.not_ge",
                        # "input": "-1",
                        # "url": None
                    }
                ]
            }
        }
    )


ProductError400 = ErrorClass("product", 400)
ProductError401 = ErrorClass("product", 401)
ProductError403 = ErrorClass("product", 403)
ProductError404 = ErrorClass("product", 404)