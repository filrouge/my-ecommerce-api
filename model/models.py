from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

DB_URL = "sqlite:///E:/Blent/1 - API/my-ecommerce-api/database/ecommerce.db"

engine = create_engine(
    DB_URL, connect_args={"check_same_thread": False},
    echo=False
    )
SessionLocal = scoped_session(
    sessionmaker(bind=engine, autoflush=False, autocommit=False)
    )


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)  # Contrainte d'unicité ?
    email = Column(String(120), unique=True, nullable=False)  # Contrainte d'unicité ?
    # Hashed during registering 
    password_hash = Column(String(255), nullable=False)
    nom = Column(String(80), nullable=False)
    role = Column(String(20), default="client")
    date_creation = Column(DateTime, nullable=False, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "nom": self.nom,
            "role": self.role,
            "date_creation": self.date_creation.isoformat()
        }
