from model.database import Base
from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    DateTime,
    ForeignKey
)
from datetime import datetime, UTC
from sqlalchemy.orm import relationship
# from sqlalchemy import UniqueConstraint


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    # Hashed during registering
    password_hash = Column(String(255), nullable=False)
    nom = Column(String(80), nullable=False)
    role = Column(String(20), default="client")
    date_creation = Column(DateTime, nullable=False, default=datetime.now(UTC))

    # orders = relationship("Order", back_populates="user")

    # Contrainte d'unicité pour l'e-mail/id:
    # __table_args__ = (
    #     UniqueConstraint("email", "id"),
    # )

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "role": self.role,
            "date_creation": self.date_creation.isoformat()
        }


class Product(Base):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True)
    nom = Column(String(120), nullable=False)
    description = Column(String(255))
    categorie = Column(String(50))
    prix = Column(Float, nullable=False)
    quantite_stock = Column(Integer, default=0)

    # orderitem = relationship("OrderItem", back_populates="product")

    # Contrainte d'unicité pour id:
    # __table_args__ = (
    #     UniqueConstraint("id"),
    # )

    def to_dict(self):
        return {
            "id": self.id,
            "nom": self.nom,
            "description": self.description,
            "categorie": self.categorie,
            "prix": self.prix,
            "quantite_stock": self.quantite_stock
        }


class Order(Base):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True)
    utilisateur_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    adresse_livraison = Column(String(255), nullable=False)
    statut = Column(String(50), default="En attente")
    date_commande = Column(Date)

    # user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

    # Contrainte d'unicité pour l'id:
    # __table_args__ = (
    #     UniqueConstraint("id"),
    # )

    def to_dict(self):
        return {
            "id": self.id,
            "utilisateur_id": self.utilisateur_id,
            "adresse_livraison": self.adresse_livraison,
            "statut": self.statut,
            "date_commande": self.date_commande.isoformat()
        }


class OrderItem(Base):
    __tablename__ = 'item_order'

    id = Column(Integer, primary_key=True)
    commande_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    produit_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantite = Column(Integer, nullable=False)
    prix_unitaire = Column(Float, nullable=False)

    # product = relationship("Product", back_populates="orderitem")
    order = relationship("Order", back_populates="items")

    # Contrainte d'unicité pour l'id:
    # __table_args__ = (
    #     UniqueConstraint("id"),
    # )

    def to_dict(self):
        return {
            "id": self.id,
            "commande_id": self.commande_id,
            "produit_id": self.produit_id,
            "quantite": self.quantite,
            "prix_unitaire": self.prix_unitaire
        }
