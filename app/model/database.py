from app.config import Config
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session

DB_URL = Config.DATABASE_URL

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
    bind=engine,
    autoflush=False,
    autocommit=False
)

Base = declarative_base()
