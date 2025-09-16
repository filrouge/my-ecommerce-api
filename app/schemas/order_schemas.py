from pydantic import BaseModel, Field, ConfigDict, field_validator, RootModel
from typing import List, Literal
from datetime import datetime
from email.utils import parsedate_to_datetime

OrderStatusLiteral = Literal["En attente", "Validée", "Expédiée", "Annulée"]


class OrderItemSchema(BaseModel):
    produit_id: int
    quantite: int = Field(..., ge=0)

    # model_config = {"from_attributes": True}
    model_config = ConfigDict(from_attributes=True)

class OrderItemRespSchema(BaseModel):
    id: int
    produit_id: int
    quantite: int  #conint(gt=0, le=10)

    model_config = ConfigDict(from_attributes=True)

# class OrderBase(BaseModel):
#     adresse_livraison: str
#     lignes: List[OrderItemSchema] = []

#     model_config = ConfigDict(from_attributes=True)

class OrderCreateSchema(BaseModel):
    adresse_livraison: str = Field(..., min_length=1)
    produits: List[OrderItemSchema]

    # model_config = {"from_attributes": True}
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "adresse_livraison": "10 rue de Paris, 75000 Paris",
                "produits": [
                    {"produit_id": 1, "quantite": 2},
                    {"produit_id": 2, "quantite": 1}
                ]
            }
        }
    )

class OrderUpdateSchema(BaseModel):
    statut: OrderStatusLiteral

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "statut": "Validée"
            }
        }
    )

class OrderRespSchema(BaseModel):
    id: int
    utilisateur_id: int
    adresse_livraison: str
    statut: str
    date_commande: datetime
    lignes: List[OrderItemSchema] = []

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "utilisateur_id": 1,
                "adresse_livraison": "10 rue de Paris, 75000 Paris",
                "statut": "En attente",
                "date_commande": "2025-09-14T14:00:00",
                "lignes": [
                    {"produit_id": 1, "quantite": 2},
                    {"produit_id": 2, "quantite": 1}
                ]
            }
        }
    )

    @field_validator("date_commande", mode="before")
    def parse_date_commande(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, str):
            try:
                return parsedate_to_datetime(v)
            except Exception:
                return datetime.fromisoformat(v)
        return v

class OrderCreateRespSchema(BaseModel):
    message: str
    commande: OrderRespSchema

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Commande créée",
                "commande": OrderRespSchema.model_json_schema()["example"]
            }
        }
    )

class OrderUpdateRespSchema(BaseModel):
    message: str
    commande: OrderUpdateSchema

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "message": "Commande mise à jour",
                "commande": OrderUpdateSchema.model_json_schema()["example"]
            }
        }
    )

class OrderListSchema(RootModel[list[OrderRespSchema]]):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "commandes": [OrderRespSchema.model_json_schema()["example"]]
            }
        }
    )
