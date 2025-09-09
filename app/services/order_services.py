from datetime import datetime, UTC
from app.model.models import Order, OrderItem, User
from app.services.product_services import get_product_id
from app.core.exceptions.app_errors import NotFoundError, BadRequestError
from sqlalchemy.orm import Session
from typing import List, Optional


def get_order_by_user(session: Session,
                      user_id: int) -> List[Order]:
    """
    Retourne la liste des commandes d'un client (ou None).
    """
    return session.query(Order).filter_by(utilisateur_id=user_id).all()


def get_all_orders(session: Session,
                   user: Optional[User] = None) -> List[Order]:
    """
    Retourne toutes les commandes si admin ou celles d'un client.

    Lève une erreur de permissions si client non autorisé
    """
    if user and user.role != "admin":
        return session.query(Order).filter_by(utilisateur_id=user.id).all()
    return session.query(Order).all()


def get_order_by_id(session: Session, order_id: int) -> Order:
    """
    Récupère une commande par son ID.

    Lève une erreur si commande introuvable
    """
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        raise NotFoundError("Commande introuvable")
    return order


def create_new_order(session: Session, user_id: int,
                     address: str, items: List[dict]) -> Order:
    """
    Crée une nouvelle commande avec ses lignes, et met à jour le stock.

    Lève une erreur si stock insuffisant
    """
    order = Order(
        utilisateur_id=user_id,
        adresse_livraison=address,
        statut="En attente",
        date_commande=datetime.now(UTC).date()
    )
    session.add(order)
    session.flush()  # génère l'ID de la commande

    for item in items:
        product = get_product_id(session, item["produit_id"])

        if product.quantite_stock < item["quantite"]:
            raise BadRequestError(
                f"Stock insuffisant pour le produit {product.nom}"
                )

        order_item = OrderItem(
            commande_id=order.id,
            produit_id=product.id,
            quantite=item["quantite"],
            prix_unitaire=product.prix
        )
        session.add(order_item)

        product.quantite_stock -= order_item.quantite

    session.flush()
    return order


def get_orderitems_all(session: Session,
                       order_id: int) -> List[OrderItem]:
    """
    Retourne toutes les lignes d'une commande.

    Lève une erreur si aucune ligne trouvée
    """
    items = session.query(OrderItem).filter_by(commande_id=order_id).all()
    if not items:
        raise NotFoundError(("Ligne de commande introuvable"))

    return items


def change_status_order(session: Session,
                        order_id: int, new_status: str) -> Order:
    """
    Modifie le statut d'une commande.
    """
    order = get_order_by_id(session, order_id)
    order.statut = new_status

    session.flush()
    session.refresh(order)
    return order
