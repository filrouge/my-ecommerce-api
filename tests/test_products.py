from model.models import Product
from typing import Tuple, Dict
from flask.testing import FlaskClient
from sqlalchemy.orm import Session
import pytest


class TestProductList:

    def test_list_all_products(
            self, test_client: Tuple[FlaskClient, Session], feed_product: list) -> None:
        client, _ = test_client

        resp = client.get("/api/produits")
        data = resp.get_json()
        assert resp.status_code == 200
        assert len(data) >= 4
        assert any(p["nom"] == feed_product[0].nom for p in data)

    def test_search_products(
            self, test_client: Tuple[FlaskClient, Session], feed_product:list ) -> None:
        client, _ = test_client

        resp = client.get("/api/produits/search?nom={feed_product[0].nom}")
        data = resp.get_json()
        assert resp.status_code == 200
        assert all(p["nom"] == feed_product[0].nom for p in data)

        resp = client.get("/api/produits/search?categorie={feed_product[1].categorie}")
        data = resp.get_json()
        assert resp.status_code == 200
        assert all(p["categorie"] == feed_product[1].categorie for p in data)

        resp = client.get("/api/produits/search?disponible=true")
        data = resp.get_json()
        assert resp.status_code == 200
        assert all(p["quantite_stock"] > 0 for p in data)
        assert len(data) >= 4


class TestProductCreate:

    @pytest.mark.parametrize("payload", [
    {"nom": "NewProduct1", "description": "Desc1", "categorie": "CatX", "prix": 15.0, "quantite_stock": 10},
    {"nom": "NewProduct2", "description": "Desc2", "categorie": "CatY", "prix": 20.0, "quantite_stock": 5}
    ])
    def test_create_product_admin(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str, payload: list
    ) -> None:
        client, _ = test_client
        resp = client.post("/api/produits", json=payload, headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert resp.status_code == 201

        data = resp.get_json()
        assert data["produit"]["nom"] == payload["nom"]
        assert "description" in data["produit"]
        assert len(data) == 2

    def test_create_product_non_admin(
        self, test_client: Tuple[FlaskClient, Session], client_token: str
    ) -> None:
        client, _ = test_client
        payload = {
            "nom": "ForbiddenProduct",
            "description": "Desc",
            "categorie": "CatX",
            "prix": 10.0,
            "quantite_stock": 5
        }
        resp = client.post("/api/produits", json=payload, headers={
            "Authorization": f"Bearer {client_token}"
        })
        assert resp.status_code == 403

    @pytest.mark.parametrize("payload", [
        {"nom": "NewProduct", "categorie": "Cat1", "prix": 15.0, "quantite_stock": 10},
        {"nom": "NewProduct", "categorie": "Cat2", "prix": 20.0, "quantite_stock": 0},
    ])
    def test_create_product_optional_field(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str, payload: list
    ) -> None:
        client, session = test_client

        resp = client.post("/api/produits", json=payload, headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert resp.status_code == 201

        data = resp.get_json()
        assert data["produit"]["nom"] == payload["nom"]
        assert "description" in data["produit"]
        assert data["produit"]["description"] == ''

        products = session.query(Product).filter(Product.categorie.in_(["Cat1", "Cat2"])).all()
        assert all(p.description is not None for p in products)
        assert all(p.description == '' for p in products)


    @pytest.mark.parametrize("payload", [
        {"categorie": "Cat1", "prix": 15.0, "quantite_stock": 10},
        {"nom": "NewProduct", "categorie": "Cat2", "quantite_stock": 0},
    ])
    def test_create_product_missing_field(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str, payload: list
    ) -> None:
        client, session = test_client

        resp = client.post("/api/produits", json=payload, headers={
            "Authorization": f"Bearer {admin_token}"
        })
        assert resp.status_code == 400

        data = resp.get_json()
        assert "error" in data
        assert "Champ(s) manquant(s)" in data["error"]
        assert any(field in data["error"] for field in ["prix", "nom"])

class TestProductUpdate:

    @pytest.mark.parametrize("payload, new_price", [
        ({"nom": "ProdUpdate", "description": "NewDesc", "prix": 6.0}, 6.0),
        ({"nom": "ProdUpdate", "description": "UpdatedAgain", "prix": 8.5}, 8.5),
    ])
    def test_update_product_by_admin(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str,
        payload: Dict, new_price: int | float) -> None:
        client, session = test_client
        product = Product(nom="ProdUpdate", description="Old",
                          categorie="CatOld", prix=5.0, quantite_stock=2
                          )
        session.add(product)
        session.commit()
        # session.flush()

        resp = client.put(f"/api/produits/{product.id}",
                          json=payload,
                          headers={"Authorization": f"Bearer {admin_token}"}
                          )
        data = resp.get_json()
        updated = session.get(Product, product.id)
        assert resp.status_code == 200
        assert data['produit']["description"] == payload["description"]
        assert updated is not None
        assert updated.prix == new_price

    @pytest.mark.parametrize("prix", [-6.0, None, 'str'])
    def test_wrong_update_product(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str, prix: list
    ) -> None:
        client, session = test_client
        product = Product(nom="ProdUpdate", description="Old",
                          categorie="CatOld", prix=5.0, quantite_stock=2
                          )
        session.add(product)
        session.commit()
        # session.flush()

        payload = {"nom": "ProdUpdate", "description": "NewDesc", "prix": prix}
        resp = client.put(f"/api/produits/{product.id}",
                          json=payload,
                          headers={"Authorization": f"Bearer {admin_token}"}
                          )
        assert resp.status_code == 400

        data = resp.get_json()
        print(data)
        assert "error" in data
        assert any(field in data["error"] for field in ["vide", "int ou float", "valeur négative"])

    def test_update_product_by_client(
        self, test_client: Tuple[FlaskClient, Session], client_token: str, feed_product: list) -> None:
        client, _ = test_client
        product = feed_product[0]

        payload = {"nom": "ProdUpdate", "description": "NewDesc", "prix": 6.0}
        resp = client.put(f"/api/produits/{product.id}",
                          json=payload,
                          headers={"Authorization": f"Bearer {client_token}"}
                          )
        assert resp.status_code == 403

        data = resp.get_json()
        assert "error" in data
        assert data["error"] == "Accès refusé"


class TestProductDelete:

    def test_delete_product_by_admin(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str, feed_product: list
    ) -> None:
        client, session = test_client
        product = feed_product[0]

        resp = client.delete(f"/api/produits/{product.id}",
                             headers={"Authorization": f"Bearer {admin_token}"}
                             )
        deleted = session.query(Product).filter_by(id=product.id).first()
        assert resp.status_code == 200
        assert deleted is None

    def test_delete_product_by_client(
        self, test_client: Tuple[FlaskClient, Session], client_token: str, feed_product: list
    ) -> None:
        client, session = test_client
        product = feed_product[0]

        resp = client.delete(f"/api/produits/{product.id}", headers={
            "Authorization": f"Bearer {client_token}"
        })
        assert resp.status_code == 403

        data = resp.get_json()
        assert "error" in data
        assert data["error"] == "Accès refusé"

        deleted = session.query(Product).filter_by(id=product.id).first()
        assert deleted is not None

    def test_delete_invalid_product(
        self, test_client: Tuple[FlaskClient, Session], admin_token: str
    ) -> None:
        client, _ = test_client
        
        resp = client.delete("/api/produits/99999",
                             headers={"Authorization": f"Bearer {admin_token}"}
                             )
        assert resp.status_code == 404

        data = resp.get_json()
        assert data["error"] == "Produit introuvable"
        
