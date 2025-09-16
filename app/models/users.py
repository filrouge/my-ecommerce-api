from __future__ import annotations

from app.database.base import Base
from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


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
