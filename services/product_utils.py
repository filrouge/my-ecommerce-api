from model.models import Product
from core.errors_handlers import NotFoundError, BadRequestError
from core.request_utils import PRODUCT_FIELDS


def get_all_products(session):
    """ Retourne la liste complète des produits. """
    return session.query(Product).all()


def get_product_id(session, produit_id):
    """ Recherche un produit par son id. """
    product = session.query(Product).filter_by(id=produit_id).first()
    if not product:
        raise NotFoundError("Produit introuvable")
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
    updated_data = {k: v for k, v in kwargs.items() if k in PRODUCT_FIELDS}

    if not updated_data or not any(updated_data.values()):
        raise BadRequestError("Aucune donnée valide pour la mise à jour")

    for field in ("prix", "quantite_stock"):
        if (value := updated_data.get(field)) is not None and value < 0:
            raise BadRequestError(f"{field.capitalize()} invalide")

    for field, value in updated_data.items():
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
