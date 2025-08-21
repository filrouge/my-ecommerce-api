'''
    Point d'entrée pour la création d'une session SQLAlchemy
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from sqlalchemy.orm import declarative_base


DB_URL = Config.DATABASE_URL

# Engine pour la database SQLite locale
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False
    )

# Creation d'une session individuelle
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Initialisation de la base
Base = declarative_base()
