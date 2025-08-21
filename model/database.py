'''
    Point d'entrée pour la création de session SQLAlchemy
'''
from config import Config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base


DB_URL = Config.DATABASE_URL

# Engine pour la database locale SQLite
engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False
    )

# Creation de session individuelle
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Initialisation de la base
Base = declarative_base()
