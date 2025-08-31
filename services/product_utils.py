from model.models import Product


def get_all_products(session):
    """ Retourne la liste complète des produits. """
    return session.query(Product).all()


def get_product_id(session, produit_id):
    """ Recherche un produit par son id. """
    product = session.query(Product).filter_by(id=produit_id).first()
    if not product:
        # raise ValueError(f"Produit ID {produit_id} introuvable")
        raise ValueError("Produit introuvable")
    return product


def add_product(session, nom, description, categorie, prix, quantite_stock):
    """ Crée un nouveau produit dans la base. """
    product = Product(
        nom=nom,
        description=description,
        categorie=categorie,
        prix=prix,
        quantite_stock=quantite_stock
    )

    session.add(product)
    session.commit()
    # session.flush()
    session.refresh(product)
    return product


def update_product(session, produit_id, **kwargs):
    """ Met à jour un produit avec les champs passés en kwargs. """
    product = get_product_id(session, produit_id)

    if "prix" in kwargs and kwargs["prix"] < 0:
        raise ValueError("Prix invalide")

    if "quantite_stock" in kwargs and kwargs["quantite_stock"] < 0:
        raise ValueError("Quantité invalide")

    for field in ["nom", "description", "categorie", "prix", "quantite_stock"]:
        if field in kwargs:
            setattr(product, field, kwargs[field])

    session.commit()
    # session.flush()
    session.refresh(product)
    return product


def delete_product_id(session, produit_id):
    """ Supprime un produit par son ID. """
    product = get_product_id(session, produit_id)

    session.delete(product)
    session.commit()
    # session.flush()
    return True


def search_product(session, nom=None, categorie=None, disponible=False):
    """ Liste les produits selon le nom, la categorie et la disponibilité. """
    query = session.query(Product)

    if nom:
        query = query.filter(Product.nom.ilike(f"%{nom}%"))

    if categorie:
        query = query.filter(Product.categorie.ilike(f"%{categorie}%"))

    if disponible:
        query = query.filter(Product.quantite_stock > 0)

    return query.all()
