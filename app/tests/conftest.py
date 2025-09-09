import pytest
from flask import g
from sqlalchemy.orm import Session
from app.model.database import Base, engine, SessionLocal
from app.model.models import User, Product, Order, OrderItem
from app.core.auth_utils import generate_token
from werkzeug.security import generate_password_hash
from app.services.product_utils import add_product
from app.services.order_utils import create_new_order, get_orderitems_all

from flask.testing import FlaskClient
from typing import Tuple, Generator, List, Dict, Any
from app import create_app
import os

# Force TestConfig à la creation de app
os.environ["FLASK_ENV"] = "testing"


@pytest.fixture(scope="session")
def setup_db() -> Generator[Tuple, None, None]:
    """
    Initialise l’application Flask et une base SQLite en mémoire pour
    la session de tests, puis détruit les tables en fin de session.

    Retourne un tuple :
        - Flask app (configurée pour les tests)
        - SessionLocal (définie fois dans database.py)
    """
    app = create_app()
    app.config["TESTING"] = True
   
    Base.metadata.create_all(bind=engine)
    yield app, SessionLocal

    Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def test_client(setup_db) -> Generator[Tuple[FlaskClient, Session],
                                       None, None]:
    """
    Crée un client de test Flask et une session SQLAlchemy pour chaque test
    (transaction avec rollback/fermeture automatique en fin d’exécution).

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
def admin_token(test_client) -> str:
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
def client_token(test_client) -> str:
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


@pytest.fixture(scope="function")
def feed_product(test_client) -> List[Product]:
    """
    Crée 4 produits distincts en alimentant la table 'product'.

    Retourne une liste contenant les 4 produits et leurs données.
    """
    _, session = test_client
    session.query(Product).delete()
    session.commit()

    p1 = add_product(session, nom="Produit A", description="Desc A",
                     categorie="Cat A", prix=20.0, quantite_stock=5)

    p2 = add_product(session, nom="Produit B", description="Desc B",
                     categorie="Cat B", prix=15.0, quantite_stock=10)

    p3 = add_product(session, nom="Produit C", description="Desc C",
                     categorie="Cat C", prix=30.0, quantite_stock=7)

    p4 = add_product(session, nom="Produit D", description="Desc D",
                     categorie="Cat D", prix=12.0, quantite_stock=8)

    return [p1, p2, p3, p4]


@pytest.fixture(scope="function")
def feed_order(test_client, client_token, feed_product) -> Dict[str, Any]:
    """
    Crée 2 commandes distinctes avec 2 lignes chacune (et 2 produits/ligne).
    Retourne un dictionnaire avec commandes, lignes de commande et client.
    """
    _, session = test_client
    user = session.query(User).filter_by(email="client@test.com").first()
    session.query(OrderItem).delete()
    session.query(Order).delete()
    session.commit()

    orders_data = []
    bodys = [
        {
            "address": "1 rue des tests",
            "produits": [
                {"produit_id": feed_product[0].id, "quantite": 1},
                {"produit_id": feed_product[1].id, "quantite": 2}
            ]
        },

        {
            "address": "123 rue des tests",
            "produits": [
                {"produit_id": feed_product[2].id, "quantite": 3},
                {"produit_id": feed_product[3].id, "quantite": 4}
            ]
        }
    ]

    for body in bodys:
        address = body.get("address")
        produits = body.get("produits")

        # Evite "cast" sur body.get() -> typer Optional
        assert isinstance(address, str)
        assert isinstance(produits, list)

        order = create_new_order(session, user.id, address, produits)
        items = get_orderitems_all(session, order.id)
        orders_data.append({"commande": order, "lignes": items})

    return {
        "commandes": orders_data,
        "utilisateur_id": user.id,
        "email": user.email
        }


# @pytest.fixture(scope="function")
# def visitor_only(test_client):
#     """
#     Crée un utilisateur sans authentification ni autorisation.
#     """
#     return None
