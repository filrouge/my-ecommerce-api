import pytest
from flask import g
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app import create_app
from model.database import Base
from model.models import User, Product, Order, OrderItem
from core.auth_utils import generate_token
from werkzeug.security import generate_password_hash
from services.product_utils import add_product
from services.order_utils import create_new_order, get_orderitems_all


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


# TODO: Modifier les tests avec ces fixtures !
##############################################
@pytest.fixture(scope="function")
def visitor_only(test_client):
    """ Crée un utilisateur pour accès sans authentification. """
    return None


@pytest.fixture(scope="function")
def feed_product(test_client):
    """
    Crée 4 produits distincts en alimentant la table 'product'.
    Retourne une liste contenant les 4 produits et leurs données.
    """
    _, session = test_client
    session.query(Product).delete()
    session.commit()

    p1 = add_product(session, "Produit A", "Desc A", "Cat A", 20.0, 5)
    p2 = add_product(session, "Produit B", "Desc B", "Cat B", 15.0, 10)
    p3 = add_product(session, "Produit C", "Desc C", "Cat C", 30.0, 7)
    p4 = add_product(session, "Produit D", "Desc D", "Cat D", 12.0, 8)

    return [p1, p2, p3, p4]


@pytest.fixture(scope="function")
def feed_order(test_client, client_token, feed_product):
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
        order = create_new_order(session, user.id,
                                 body["address"],
                                 body["produits"]
                                 )
        items = get_orderitems_all(session, order.id)
        orders_data.append({"order": order, "items": items})

    return {"orders": orders_data,
            "user_id": user.id,
            "user_email": user.email
            }
