from pydantic import BaseModel, ConfigDict
from typing import Any, Tuple, Optional

class ValidationErrorItem(BaseModel):
    loc: Tuple[Any, ...]           # Champ(s) en erreur
    msg: str                       # Message d'erreur
    type: str                      # Type d'erreur Pydantic
    # ctx: Optional[Dict[str, Any]] = None
    input: Optional[Any] = None    # Entrée qui a provoqué l'erreur
    url: Optional[str] = None      # Lien doc Pydantic

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "loc": ("prix",),
                "msg": "Input should be a valid number",
                "type": "float_parsing",
                "input": "str",
                "url": "https://errors.pydantic.dev/2.11/v/float_parsing"
            }
        }
    )

class ValidationErrorsSchema(BaseModel):
    errors: list[ValidationErrorItem]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "errors": [
                    ValidationErrorItem.model_json_schema()["example"]
                ]
            }
        }
    )