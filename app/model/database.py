from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

from app.config import CONFIG_MAP
import os

# Choix de la config active selon FLASK_ENV
ENV = os.getenv("FLASK_ENV", "dev").lower()
app_config = CONFIG_MAP.get(ENV, CONFIG_MAP["dev"])

'''
Point d'entrée pour la création de session SQLAlchemy:
    - Engine pour database locale SQLite
    - Creation de session individuelle
    - Initialisation de la base
'''
DB_URL = app_config.DATABASE_URL

engine: Engine = create_engine(
    DB_URL,
    connect_args={"check_same_thread": False},
    echo=False
    )

# autoflush=True, autocommit=True -> souci commit() en PROD ?
SessionLocal: sessionmaker[Session] = sessionmaker(
    bind=engine, autoflush=False, autocommit=False
)

Base = declarative_base()
