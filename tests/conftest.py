import pytest
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app
from model.database import Base


@pytest.fixture(scope="session")
def setup_db():
    """
    Crée l'app Flask et la database SQLite (en mémoire) pour la
    session de tests et détruit la database en fin de session.
    """
    app = create_app()
    app.config["TESTING"] = True

    # Engine (forcé en mémoire) et session de test isolée
    engine = create_engine("sqlite:///:memory:", echo=False)
    SessionLocal = sessionmaker(bind=engine)

    # Création des tables et Provision du engine/session
    Base.metadata.create_all(bind=engine)
    yield app, SessionLocal

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(setup_db):
    """
    Retourne un tuple (FlaskClient et session SQLAlchemy) de test, qui
    gère le app.app_context() et ouvre une transaction isolée par test
    (avec rollback et fermeture automatique après chaque test) avec
    remise de g.session à la session courante avant chaque test :
        - client : client de test pour simuler des requêtes HTTP
        - session : sert à interroger la base de test
    """

    app, SessionLocal = setup_db

    with app.app_context():
        session = SessionLocal()
        g.session = session

        try:
            with app.test_client() as client:
                yield client, session

            session.rollback()

        finally:
            session.close()
            g.pop("session", None)
