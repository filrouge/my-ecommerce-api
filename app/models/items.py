from __future__ import annotations

from app.database.base import Base
from sqlalchemy import Integer, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItem(Base):
    __tablename__ = 'order_item'

    id: Mapped[int] = mapped_column(primary_key=True)
    commande_id: Mapped[int] = mapped_column(Integer, ForeignKey("order.id"),
                                             nullable=False)
    produit_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"),
                                            nullable=False)
    quantite: Mapped[int] = mapped_column(Integer, nullable=False)
    prix_unitaire: Mapped[float] = mapped_column(Float, nullable=False)

    product: Mapped["Product"] = relationship(
        "Product", back_populates="orderitem")
    order: Mapped["Order"] = relationship("Order", back_populates="items")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "commande_id": self.commande_id,
            "produit_id": self.produit_id,
            "quantite": self.quantite,
            "prix_unitaire": self.prix_unitaire,
            "produit_nom": self.product.nom if self.product else None
        }
