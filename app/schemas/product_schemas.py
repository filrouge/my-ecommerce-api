from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, model_validator, RootModel


class ProductCreateSchema(BaseModel):
    nom: str = Field(..., min_length=1)
    description: Optional[str] = Field(default=None)
    categorie: Optional[str] = Field(default=None)
    prix: float = Field(..., gt=0)
    quantite_stock: int = Field(..., ge=0)

    @model_validator(mode="before")
    def normalize_strings(cls, values):
        for field in ["description", "categorie"]:
            if values.get(field) in (None, ""):
                values[field] = ""
        return values

    model_config = ConfigDict(from_attributes=True,
        json_schema_extra={
            "example": {
                "nom": "Laptop",
                "description": "PC portable",
                "categorie": "Informatique",
                "prix": 1299.99,
                "quantite_stock": 10
            }
        }
    )


class ProductUpdateSchema(BaseModel):
    nom: Optional[str] = None
    description: Optional[str] = None
    categorie: Optional[str] = None
    prix: Optional[float] = Field(None, gt=0)
    quantite_stock: Optional[int] = Field(None, ge=0)

    @model_validator(mode="before")
    def at_least_one_field(cls, values):
        if not any(v is not None for v in values.values()):
            raise ValueError("Au moins un champ doit être fourni pour la mise à jour")
        return values
    
    model_config = ConfigDict(from_attributes=True,
        json_schema_extra={
            "example": {
                "nom": "Laptop Updated",
                "description": "PC portable amélioré",
                "categorie": "Informatique",
                "prix": 1399.99,
                "quantite_stock": 8
            }
        }
    )


class ProductRespSchema(BaseModel):
    id: int
    nom: str
    description: str
    categorie: str
    prix: float
    quantite_stock: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "nom": "Laptop",
                "description": "PC portable",
                "categorie": "Informatique",
                "prix": 1299.99,
                "quantite_stock": 10
            }
        }
    )


class ProductCreateRespSchema(BaseModel):
    message: str
    produit: ProductRespSchema

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Produit ajouté",
                "produit": ProductRespSchema.model_json_schema()["example"]
            }
        }
    )


class ProductUpdateRespSchema(BaseModel):
    message: str
    produit_id: int
    produit: ProductRespSchema

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Produit mis à jour",
                "produit_id": 1,
                "produit": ProductRespSchema.model_json_schema()["example"]
            }
        }
    )


class ProductDeleteRespSchema(BaseModel):
    message: str
    deleted_id: int

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Produit 1 supprimé",
                "deleted_id": 1
            }
        }
    )


# RootModel pour renvoyer liste de produits
class ProductListSchema(RootModel[list[ProductRespSchema]]):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": [
                ProductRespSchema.model_json_schema()["example"],
                ProductRespSchema.model_json_schema()["example"]
            ]
        }
    )
