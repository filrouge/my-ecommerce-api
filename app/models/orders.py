from __future__ import annotations
from app.database.base import Base
from datetime import datetime, timezone
from sqlalchemy import Integer, String, ForeignKey, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Order(Base):
    __tablename__ = 'order'

    STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]

    id: Mapped[int] = mapped_column(primary_key=True)
    utilisateur_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"),
                                                nullable=False)
    adresse_livraison: Mapped[str] = mapped_column(String(255), nullable=False)   
    statut: Mapped[str] = mapped_column(Enum(*STATUS, name="order_status"),
                                        default="En attente", nullable=False)
    date_commande: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        # default=lambda: datetime.now(timezone.utc).date(),
        default=datetime.now(timezone.utc),
        nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship("OrderItem",
                                                    back_populates="order",
                                                    cascade="all, delete-orphan")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "utilisateur_id": self.utilisateur_id,
            "adresse_livraison": self.adresse_livraison,
            "statut": self.statut,
            "date_commande": self.date_commande.isoformat() if
            self.date_commande else None,
            "lignes": [item.to_dict() for item in self.items]
        }
