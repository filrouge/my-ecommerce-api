from model.models import Order, OrderItem, Product, User
import jwt
from core.auth_utils import JWT_KEY, ALGORITHM


class TestOrderCreation:

    def test_client_create_order(self, test_client, client_token):
        client, session = test_client

        # Récupération de l'user_id depuis le token JWT
        payload_token = jwt.decode(
            client_token, JWT_KEY, algorithms=[ALGORITHM]
            )
        user_id = payload_token["id"]

        # Ajout de produits
        p1 = Product(
            nom="Produit A",
            description="Desc A",
            categorie="test",
            prix=20.0,
            quantite_stock=5
        )
        p2 = Product(
            nom="Produit B",
            description="Desc B",
            categorie="test",
            prix=15.0,
            quantite_stock=10
        )
        session.add_all([p1, p2])
        session.commit()

        payload = {
            "adresse_livraison": "123 rue des tests",
            "produits": [
                {"produit_id": p1.id, "quantite": 2},
                {"produit_id": p2.id, "quantite": 1},
            ]
        }
        resp = client.post(
            "/api/commandes",
            json=payload,
            headers={"Authorization": f"Bearer {client_token}"}
            )
        assert resp.status_code == 201
        data = resp.get_json()
        db_order = session.get(Order, data["commande"]["id"])

        assert "message" in data
        assert "id" in data["message"]
        assert data["message"].startswith("Commande")
        assert data["commande"]["statut"] == "En attente"

        # Vérifie si la commande existe en base
        assert db_order is not None
        assert len(db_order.items) == 2
        assert db_order.statut == "En attente"
        assert db_order.adresse_livraison == payload["adresse_livraison"]
        assert db_order.utilisateur_id == user_id


class TestOrderSearch:

    def test_client_own_orders(self, test_client, client_token):
        client, _ = test_client
        headers = {"Authorization": f"Bearer {client_token}"}
        resp = client.get("/api/commandes", headers=headers)
        assert resp.status_code == 200
        commandes = resp.get_json()
        assert isinstance(commandes, list)

    def test_admin_all_orders(self, test_client, admin_token):
        client, _ = test_client
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.get("/api/commandes", headers=headers)
        assert resp.status_code == 200
        commandes = resp.get_json()
        assert isinstance(commandes, list)


class TestOrderItems:

    def test_access_orderitems(self, test_client, client_token):
        client, session = test_client

        produit = Product(
            nom="ProduitC",
            description="Desc",
            categorie="Cat",
            prix=30.0,
            quantite_stock=3
        )
        session.add(produit)
        session.commit()

        payload = {
            "adresse_livraison": "Avenue Test",
            "produits": [
                {"produit_id": produit.id, "quantite": 1}
                ]
        }
        headers = {"Authorization": f"Bearer {client_token}"}
        resp = client.post("/api/commandes", json=payload, headers=headers)
        order_id = resp.get_json()["commande"]["id"]

        # Consultation des lignes d'une commande
        resp_items = client.get(f"/api/commandes/{order_id}/lignes")
        items = resp_items.get_json()
        assert resp_items.status_code == 200
        assert isinstance(items, list)
        assert len(items) == 1

    def test_missing_orderitems(self, test_client):
        client, _ = test_client
        resp = client.get("/api/commandes/999/lignes")
        assert resp.status_code == 404


class TestOrderUpdate:

    def test_admin_update_status(self, test_client, admin_token):
        client, session = test_client

        # Ajout de produit
        product = Product(
            nom="Produit",
            description="Desc",
            categorie="Cat",
            prix=50.0,
            quantite_stock=2
        )
        session.add(product)
        session.commit()

        # # Récupération de l'user_id depuis le token JWT
        # payload_token = jwt.decode(
        #     admin_token, JWT_KEY, algorithms=[ALGORITHM]
        #     )
        # admin_id = payload_token["id"]

        admin = session.query(User).filter_by(email="admin@test.com").first()
        admin_id = admin.id

        # Création de 2 commandes
        order1 = Order(
            utilisateur_id=admin_id,
            adresse_livraison="Rue X",
            statut="En attente"
        )
        order2 = Order(
            utilisateur_id=admin_id,
            adresse_livraison="Rue Y",
            statut="En attente"
            )
        session.add_all([order1, order2])
        session.flush()

        item1 = OrderItem(
            order=order1,
            produit_id=product.id,
            quantite=1,
            prix_unitaire=product.prix
        )
        item2 = OrderItem(
            order=order1,
            produit_id=product.id,
            quantite=1,
            prix_unitaire=product.prix
        )
        session.add_all([item1, item2])
        session.commit()

        # order1_id = order1.id
        order2_id = order2.id
        product_id = product.id

        payload = {"statut": "Validée"}
        headers = {"Authorization": f"Bearer {admin_token}"}
        resp = client.patch(f"/api/commandes/{order1.id}",
                            json=payload, headers=headers
                            )

        data = resp.get_json()
        assert resp.status_code == 200
        assert data["commande"]["statut"] == "Validée"

        db_product = session.get(Product, product_id)
        assert db_product.nom == "Produit"
        assert db_product.quantite_stock == 2
        # db_order = session.get(Order, data["commande"]["id"])
        db_order1 = session.get(Order, order1.id)
        db_order2 = session.get(Order, order2_id)
        assert db_order1.statut == "Validée"
        assert db_order2.statut == "En attente"

    def test_client_update_status(self, test_client, client_token):
        client, session = test_client

        # Ajout de produit et Création de commande
        product = Product(
            nom="Produit",
            description="Desc",
            categorie="Cat",
            prix=40.0,
            quantite_stock=5
        )
        session.add(product)
        session.commit()

        payload = {
            "adresse_livraison": "Rue du Client",
            "produits": [{"produit_id": product.id, "quantite": 1}]
        }
        headers = {"Authorization": f"Bearer {client_token}"}
        resp = client.post("/api/commandes",
                           json=payload, headers=headers)

        # Tentative de mise à jour du statut
        order_id = resp.get_json()["commande"]["id"]
        payload = {"statut": "Validée"}
        resp = client.patch(f"/api/commandes/{order_id}",
                            json=payload, headers=headers)

        assert resp.status_code == 403
        data = resp.get_json()
        print(data)
        assert "error" in data and "Access denied" in data['error']
