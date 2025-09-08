from app.model.models import Order, User, Product
import jwt
from app.config import Config
from typing import Tuple
from flask.testing import FlaskClient
from sqlalchemy.orm import Session
import pytest

JWT_KEY = Config.JWT_KEY
ALGORITHM = Config.ALGORITHM


class TestOrderCreation:

    def test_client_create_order(self,
                                 test_client: Tuple[FlaskClient, Session],
                                 client_token: str,
                                 feed_product: list) -> None:
        """Un client peut créer une commande avec plusieurs produits."""
        client, session = test_client

        payload = {
            "adresse_livraison": "123 rue des tests",
            "produits": [
                {"produit_id": feed_product[0].id, "quantite": 2},
                {"produit_id": feed_product[1].id, "quantite": 1},
            ]
        }

        resp = client.post(
            "/api/commandes",
            json=payload,
            headers={"Authorization": f"Bearer {client_token}"}
            )
        assert resp.status_code == 201

        data = resp.get_json()
        assert "message" in data
        assert "id" in data["message"]
        assert data["message"].startswith("Commande")
        assert data["commande"]["statut"] == "En attente"
        assert data["commande"]["adresse_livraison"] == payload["adresse_livraison"]
        print(data["commande"])
        assert len(data["commande"]["lignes"]) == 2

        db_order = session.get(Order, data["commande"]["id"])
        assert db_order is not None
        assert len(db_order.items) == 2
        assert db_order.statut == "En attente"
        assert db_order.adresse_livraison == payload["adresse_livraison"]

        payload_token = jwt.decode(
            client_token, JWT_KEY, algorithms=[ALGORITHM]
            )
        user_id = payload_token["id"]
        assert db_order.utilisateur_id == user_id


class TestOrderSearch:

    def test_client_own_orders(self, test_client: Tuple[FlaskClient, Session],
                               client_token: str, feed_order: list) -> None:
        """Le client ne voit que ses propres commandes."""
        client, _ = test_client
        headers = {"Authorization": f"Bearer {client_token}"}
        resp = client.get("/api/commandes", headers=headers)
        assert resp.status_code == 200
        commandes = resp.get_json()
        assert isinstance(commandes, list)
        for c in commandes:
            assert c["utilisateur_id"] == feed_order["utilisateur_id"]

    def test_admin_all_orders(self, test_client: Tuple[FlaskClient, Session],
                              admin_token: str, feed_order: list) -> None:
        client, _ = test_client
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.get("/api/commandes", headers=headers)
        assert resp.status_code == 200
        commandes = resp.get_json()
        assert isinstance(commandes, list)
        all_ids = [order["commande"].id for order in feed_order["commandes"]]
        for c in commandes:
            assert c["id"] in all_ids


class TestOrderItems:

    def test_access_orderitems(self, test_client: Tuple[FlaskClient, Session],
                               client_token: str, feed_order: list) -> None:
        """Vérifie la récupération des lignes d’une commande existante."""
        client, _ = test_client

        order_id = feed_order["commandes"][0]["commande"].id

        headers = {"Authorization": f"Bearer {client_token}"}
        resp = client.get(f"/api/commandes/{order_id}/lignes", headers=headers)
        lignes = resp.get_json()
        assert resp.status_code == 200
        assert isinstance(lignes, list)
        assert len(lignes) == len(feed_order["commandes"][0]["lignes"])

    def test_missing_orderitems(
            self, test_client: Tuple[FlaskClient, object]) -> None:
        """Tentative d’accès à des lignes de commande inexistantes."""
        client, _ = test_client
        resp = client.get("/api/commandes/999/lignes")
        assert resp.status_code == 404


class TestOrderUpdate:

    def test_admin_update_status(self, test_client: Tuple[FlaskClient, Session],
                                 admin_token: str, feed_order: list) -> None:
        """L’admin peut modifier le statut d’une commande."""
        client, session = test_client

        order1 = feed_order["commandes"][0]["commande"]
        order2_id = feed_order["commandes"][1]["commande"].id
        payload = {"statut": "Validée"}
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.patch(f"/api/commandes/{order1.id}", json=payload, headers=headers)

        data = resp.get_json()
        assert resp.status_code == 200
        assert data["commande"]["statut"] == "Validée"

        # db_order1 = session.get(Order, data["commande"]["id"])
        db_order1 = session.get(Order, order1.id)
        assert db_order1 is not None
        assert db_order1.statut == "Validée"

        db_order2 = session.query(Order).filter(Order.id == order2_id).first()
        assert db_order2 is not None
        assert db_order2.statut == "En attente"

    def test_client_no_update_status(self, test_client: Tuple[FlaskClient, Session],
                                  client_token: str, feed_order: list) -> None:
        client, _ = test_client

        order = feed_order["commandes"][0]["commande"]
        payload = {"statut": "Validée"}
        headers = {"Authorization": f"Bearer {client_token}"}
        resp = client.patch(f"/api/commandes/{order.id}", json=payload, headers=headers)

        assert resp.status_code == 403
        data = resp.get_json()
        assert "error" in data and "Accès refusé" in data['error']

    @pytest.mark.parametrize("new_status", [None, "annulée"])
    def test_update_wrong_status(self,
                                 test_client: Tuple[FlaskClient, Session], admin_token: str,
                                 feed_order: list, new_status: list) -> None:

        client, session = test_client

        order = feed_order["commandes"][0]["commande"]
        payload = {"statut": new_status}
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.patch(f"/api/commandes/{order.id}", json=payload, headers=headers)

        data = resp.get_json()
        print(data)
        assert resp.status_code == 400
        assert "error" in data
        assert any(field in data["error"] for field in ['invalide', 'vide'])
        db_order = session.get(Order, order.id)
        assert db_order is not None and db_order.statut == "En attente"
