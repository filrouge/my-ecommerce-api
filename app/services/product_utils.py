from app.model.models import Product
from app.core.exceptions.app_errors import NotFoundError
from sqlalchemy.orm import Session
from typing import List, Optional


def get_all_products(session: Session) -> List[Product]:
    """
    Retourne la liste complète des produits (None si inexistant) depuis la base.        
    """
    return session.query(Product).all()


def get_product_id(session: Session, produit_id: int) -> Product:
    """
    Retourne une instance produit par son ID.

    Lève une erreur si produit introuvable.
    """
    product = session.query(Product).filter_by(id=produit_id).first()
    if not product:
        raise NotFoundError("Produit introuvable")
    return product


def add_product(session: Session, **kwargs) -> Product:
    """
    Crée un nouveau produit dans la base et retourne une instance produit
    """
    product = Product(**kwargs)

    session.add(product)
    session.flush()
    return product


def update_product(session: Session, produit_id: int, **kwargs) -> Product:
    """
    Met à jour un produit existant et retourne l'instance produit modifié.
    """
    product = get_product_id(session, produit_id)

    for field, value in kwargs.items():
        setattr(product, field, value)

    session.flush()
    session.refresh(product)
    return product


def delete_product_id(session: Session, produit_id: int) -> bool:
    """
    Supprime un produit de la base.
    """
    product = get_product_id(session, produit_id)

    session.delete(product)
    session.flush()
    return True


def search_product(session: Session, nom: Optional[str] = None,
                   categorie: Optional[str] = None, disponible: bool = False
                   ) -> List[Product]:
    """
    Retourne une liste de produits filtrés par nom, catégorie ou disponibilité.
    """
    query = session.query(Product)

    if nom:
        query = query.filter(Product.nom.ilike(f"%{nom}%"))

    if categorie:
        query = query.filter(Product.categorie.ilike(f"%{categorie}%"))

    if disponible:
        query = query.filter(Product.quantite_stock > 0)

    return query.all()
