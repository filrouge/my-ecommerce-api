from model.database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, UTC
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
