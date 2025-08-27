from model.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC
# from sqlalchemy import UniqueConstraint

from sqlalchemy import Float
# from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    # Hashed during registering
    password_hash = Column(String(255), nullable=False)
    nom = Column(String(80), nullable=False)
    role = Column(String(20), default="client")
    date_creation = Column(DateTime, nullable=False, default=datetime.now(UTC))

    # Contrainte d'unicité pour l'e-mail:
    # __table_args__ = (
    #     UniqueConstraint("email", name="admin"),
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

    # Add produit = relationship("OrderItem")

    # Contrainte d'unicité pour id/email:
    # __table_args__ = (
    #     UniqueConstraint("email", name="admin"),
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
