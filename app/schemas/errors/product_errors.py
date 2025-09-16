from app.schemas.errors.validation_schemas import ValidationErrorsSchema
from pydantic import ConfigDict


# CREATE
class ProductCreateError(ValidationErrorsSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("prix",),
                        "msg": "Input should be a valid number",
                        "type": "float_parsing",
                        "input": "str",
                        "url": "https://errors.pydantic.dev/2.11/v/float_parsing"
                    }
                ]
            }
        }
    )

# UPDATE
class ProductUpdateError(ValidationErrorsSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("quantite_stock",),
                        "msg": "Value must be greater than or equal to 0",
                        "type": "value_error.number.not_ge",
                        "input": "-5",
                        "url": "https://errors.pydantic.dev/2.11/v/value_error.number.not_ge"
                    }
                ]
            }
        }
    )

# DELETE
class ProductDeleteError(ValidationErrorsSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("product_id",),
                        "msg": "Produit non trouvé",
                        "type": "not_found",
                        "input": "999",
                        "url": None
                    }
                ]
            }
        }
    )

# LIST
class ProductListError(ValidationErrorsSchema):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    {
                        "loc": ("limit",),
                        "msg": "Paramètre doit être un entier positif",
                        "type": "value_error.number.not_ge",
                        "input": "-1",
                        "url": None
                    }
                ]
            }
        }
    )
