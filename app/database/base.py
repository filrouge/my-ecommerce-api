from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from config import CONFIG_MAP
import os

# Choix de la config active selon FLASK_ENV
ENV = os.getenv("FLASK_ENV", "dev").lower()
app_config = CONFIG_MAP.get(ENV, CONFIG_MAP["dev"])
DB_URL = app_config.DATABASE_URL


'''
Point d'entrée pour la création de session SQLAlchemy:
    - Engine pour database locale SQLite
    - Creation de session individuelle
    - Initialisation de la base
'''
engine: Engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False
    )

SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine, autoflush=True, autocommit=False
)

Base = declarative_base()
