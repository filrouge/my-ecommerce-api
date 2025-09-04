from model.models import Product


class TestProductList:

    def test_list_all_products(self, test_client):
        client, session = test_client

        p1 = Product(nom="Product1", description="Desc1",
                     categorie="Cat1", prix=10.0, quantite_stock=5
                     )
        p2 = Product(nom="Product2", description="Desc2",
                     categorie="Cat2", prix=20.0, quantite_stock=0
                     )
        session.add_all([p1, p2])
        session.commit()

        resp = client.get("/api/produits")
        data = resp.get_json()
        assert resp.status_code == 200
        assert len(data) >= 2
        assert any(p["nom"] == "Product1" for p in data)

    def test_search_products(self, test_client):
        client, _ = test_client

        resp = client.get("/api/produits/search?nom=Product1")
        data = resp.get_json()
        # print([p["nom"] for p in data])
        assert resp.status_code == 200
        assert all("Product1" in p["nom"] for p in data)

        resp = client.get("/api/produits/search?categorie=Cat2")
        data = resp.get_json()
        assert all(p["categorie"] == "Cat2" for p in data)

        resp = client.get("/api/produits/search?disponible=true")
        data = resp.get_json()
        assert all(p["quantite_stock"] > 0 for p in data)


class TestProductCreate:

    def test_create_product_admin(self, test_client, admin_token):
        client, session = test_client
        payload = {
            "nom": "NewProduct",
            "description": "Desc",
            "categorie": "CatX",
            "prix": 15.0,
            "quantite_stock": 10
        }
        resp = client.post("/api/produits", json=payload, headers={
            "Authorization": f"Bearer {admin_token}"
        })
        data = resp.get_json()
        # print(data["produit"]["nom"])
        product = session.query(Product).filter_by(nom=payload["nom"]).first()
        assert resp.status_code == 201
        assert data["produit"]["nom"] == payload["nom"]
        assert product is not None

    def test_create_product_non_admin(self, test_client, client_token):
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


class TestProductUpdate:

    def test_update_product(self, test_client, admin_token):
        client, session = test_client
        product = Product(nom="ProdUpdate", description="Old",
                          categorie="CatOld", prix=5.0, quantite_stock=2
                          )
        session.add(product)
        session.commit()
        # session.flush()

        payload = {"nom": "ProdUpdate", "description": "NewDesc", "prix": 6.0}
        resp = client.put(f"/api/produits/{product.id}",
                          json=payload,
                          headers={"Authorization": f"Bearer {admin_token}"}
                          )
        data = resp.get_json()
        updated = session.get(Product, product.id)
        assert resp.status_code == 200
        assert data['produit']["description"] == "NewDesc"
        assert updated.prix == 6.0

    def test_wrong_update_product(self, test_client, admin_token):
        client, session = test_client
        product = Product(nom="ProdUpdate", description="Old",
                          categorie="CatOld", prix=5.0, quantite_stock=2
                          )
        session.add(product)
        session.commit()
        # session.flush()

        # payload = {"nom": "ProdUpdate", "description": "NewDesc", "prix": -6.0}
        payload = {"nom": "ProdUpdate", "description": "NewDesc", "prix": "-6.0"}
        resp = client.put(f"/api/produits/{product.id}",
                          json=payload,
                          headers={"Authorization": f"Bearer {admin_token}"}
                          )
        data = resp.get_json()
        assert resp.status_code == 400
        assert "Prix invalide" in data["error"]


class TestProductDelete:

    def test_delete_product_by_admin(self, test_client, admin_token):
        client, session = test_client
        product = Product(nom="ProdDelete", description="Desc",
                          categorie="CatX", prix=10.0, quantite_stock=1
                          )
        session.add(product)
        session.commit()
        # session.flush()

        resp = client.delete(f"/api/produits/{product.id}",
                             headers={"Authorization": f"Bearer {admin_token}"}
                             )
        deleted = session.query(Product).filter_by(id=product.id).first()
        assert resp.status_code == 200
        assert deleted is None

    def test_delete_product_by_client(self, test_client, client_token):
        client, session = test_client
        product = Product(nom="ProdDelete", description="Desc",
                          categorie="CatX", prix=10.0, quantite_stock=1
                          )
        session.add(product)
        session.commit()
        # session.flush()

        resp = client.delete(f"/api/produits/{product.id}", headers={
            "Authorization": f"Bearer {client_token}"
        })
        deleted = session.query(Product).filter_by(id=product.id).first()
        assert resp.status_code == 403
        assert deleted is not None

    def test_delete_invalid_product(self, test_client, admin_token):
        client, _ = test_client
        resp = client.delete("/api/produits/99999",
                             headers={"Authorization": f"Bearer {admin_token}"}
                             )
        assert resp.status_code == 404
