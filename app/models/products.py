from __future__ import annotations
from app.database.base import Base
from sqlalchemy import Integer, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional


class Product(Base):
    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    nom: Mapped[str] = mapped_column(String(120), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(255),
                                                       nullable=True)
    categorie: Mapped[Optional[str]] = mapped_column(String(50),
                                                     nullable=True)
    prix: Mapped[float] = mapped_column(Float, nullable=False)
    quantite_stock: Mapped[int] = mapped_column(Integer, default=0,
                                                nullable=False)

    orderitem: Mapped[List["OrderItem"]] = relationship(
        "OrderItem", back_populates="product")

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "categorie": self.categorie,
            "prix": self.prix,
            "quantite_stock": self.quantite_stock
        }
