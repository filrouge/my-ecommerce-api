import pytest
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app
from model.database import Base
from model.models import User
from core.auth_utils import generate_token
from werkzeug.security import generate_password_hash
# from model.models import Product, Order, OrderItem


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
    Ouvre une transaction par test (avec rollback/fermeture automatique)
    avec gestion du app.app_context() et remise de la g.session à
    la session courante avant chaque test.

    Retourne un tuple (FlaskClient, session SQLAlchemy) de test :
        - client : pour simuler les requêtes HTTP
        - session : pour interroger la base de test
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


@pytest.fixture(scope="function")
def admin_token(test_client):
    """ Crée un utilisateur admin et retourne son JWT. """
    _, session = test_client
    session.query(User).filter_by(email="admin@test.com").delete()
    admin = User(
        email="admin@test.com",
        nom="Admin",
        password_hash=generate_password_hash("password123"),
        role="admin"
        )

    session.add(admin)
    session.commit()
    return generate_token(admin)


@pytest.fixture(scope="function")
def client_token(test_client):
    """ Crée un utilisateur client et retourne son JWT. """
    _, session = test_client
    session.query(User).filter_by(email="client@test.com").delete()
    user = User(
        email="client@test.com",
        nom="Client",
        password_hash=generate_password_hash("password123"),
        role="client"
        )

    session.add(user)
    session.commit()
    return generate_token(user)

###############
# TODO
# Modifier Tests
###############
# @pytest.fixture(scope="function")
# def visitor_access(test_client)::
    # """
    # Crée un visteur avec accès restreint
    # sans enregistrement ni authentification.
    # """

# @pytest.fixture(scope="function")
# def feed_products(test_client):
    # """
    # Alimente la table 'product' (4 produits distincs)
    # et retourne une liste des 4 produits.
    # """


# @pytest.fixture(scope="function")
# def feed_orders(test_client, client_token, setup_product):
    # """
    # Crée 2 commandes distinctes (2 lignes / commande, 2 produits / ligne) en
    # alimentant les tables 'order' et 'order_item' et retourne un dictionnaire
    # comprenant les commandes, l'id du client et lignes de commande
    # """
