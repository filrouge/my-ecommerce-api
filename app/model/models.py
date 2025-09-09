from __future__ import annotations

from app.model.database import Base
from datetime import datetime, date, timezone
from sqlalchemy import Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True,
                                       nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    nom: Mapped[str] = mapped_column(String(80), nullable=False)
    role: Mapped[str] = mapped_column(String(20),
                                      nullable=False, default="client")
    date_creation: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False,
        default=lambda: datetime.now(timezone.utc)
    )

    orders: Mapped[List["Order"]] = relationship("Order",
                                                 back_populates="user")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "role": self.role,
            "date_creation": self.date_creation.isoformat() if
            self.date_creation else None
        }
    
    FIELDS: dict[str, type] = {
        "email": str, "nom": str, "password": str, "role": str
        }


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
    
    FIELDS: dict[str, type | tuple[type, ...]] = {
    "nom": str, "description": str, "categorie": str, "prix": (int, float), "quantite_stock": (int)
    }


class Order(Base):
    __tablename__ = 'order'

    id: Mapped[int] = mapped_column(primary_key=True)
    utilisateur_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"),
                                                nullable=False)
    adresse_livraison: Mapped[str] = mapped_column(String(255), nullable=False)
    statut: Mapped[str] = mapped_column(String(50), default="En attente",
                                        nullable=False)
    date_commande: Mapped[date] = mapped_column(
        Date,
        default=lambda: datetime.now(timezone.utc).date(),
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
    
    FIELDS: dict[str, type] = {
    "produits": list, "adresse_livraison": str, "statut": str
    }
    STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]


class OrderItem(Base):
    __tablename__ = 'item_order'

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
    
    FIELDS: dict[str, type] = {
    "produit_id": (int), "quantite": (int),
    }
