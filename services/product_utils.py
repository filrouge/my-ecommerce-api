from model.models import Product
from core.errors_handlers import NotFoundError


def get_all_products(session):
    """ Retourne la liste complète des produits. """
    return session.query(Product).all()


def get_product_id(session, produit_id):
    """ Recherche un produit par son id. """
    product = session.query(Product).filter_by(id=produit_id).first()
    if not product:
        raise NotFoundError("Produit introuvable")
    return product


def add_product(session, **kwargs):
    """ Crée un nouveau produit dans la base. """
    product = Product(**kwargs)

    session.add(product)
    session.commit()
    # session.flush()
    session.refresh(product)
    return product


def update_product(session, produit_id, **kwargs):
    """ Met à jour un produit avec les champs passés en kwargs. """
    product = get_product_id(session, produit_id)

    for field, value in kwargs.items():
        setattr(product, field, value)

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
