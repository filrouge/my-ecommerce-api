from datetime import datetime, UTC
from model.models import Order, OrderItem
from services.product_utils import get_product_id

STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]


def get_order_by_user(session, user_id):
    """ Retourne les commandes d'un utilisateur spécifique. """
    return session.query(Order).filter_by(utilisateur_id=user_id).all()


def get_all_orders(session, user=None):
    """ Retourne toutes les commandes (admin) ou celles du client. """
    if user and user.role != "admin":
        return session.query(Order).filter_by(utilisateur_id=user.id).all()
    return session.query(Order).all()


def get_order_by_id(session, order_id):
    """ Récupère une commande par son ID. """
    order = session.query(Order).filter_by(id=order_id).first()
    if not order:
        raise ValueError("Commande introuvable")
    return order


def create_new_order(session, user_id, address, items):
    """ Crée une nouvelle commande pour un utilisateur. """
    if not items:
        raise ValueError("La commande ne contient aucune liste de produits.")

    if not address:
        raise ValueError("Adresse de livraison requise.")

    order = Order(
        utilisateur_id=user_id,
        date_commande=datetime.now(UTC).date(),
        adresse_livraison=address,
        statut="En attente"
    )
    session.add(order)
    # session.flush()  # génère l'ID de la commande
    session.commit()

    for item in items:
        if "produit_id" not in item:
            raise ValueError("Id produit manquant dans la commande")

        product = get_product_id(session, item["produit_id"])
        if product.quantite_stock < item["quantite"]:
            raise ValueError(
                f"Stock insuffisant pour le produit {product.nom}"
                )

        order_item = OrderItem(
            commande_id=order.id,
            produit_id=product.id,
            quantite=item["quantite"],
            prix_unitaire=product.prix
        )
        session.add(order_item)

        # mise à jour du stock
        product.quantite_stock -= order_item.quantite

    session.commit()
    session.refresh(order)
    return order


def get_orderitems_all(session, order_id):
    """ Retourne toutes les lignes d'une commande. """
    items = session.query(OrderItem).filter_by(commande_id=order_id).all()
    if not items:
        raise ValueError(("Ligne de commande introuvable"))

    return items


# def get_orderitem_id(session, order_id, orderitem_id):
#     """ Récupère une ligne de commande par son ID. """
#     item = session.query(OrderItem).filter_by(
#         commande_id=order_id, id=orderitem_id).first()
#     if not item:
#         raise ValueError("Ligne de commande introuvable")
#     return item


def change_status_order(session, order_id, new_status):
    """ Modifie le statut d'une commande. """
    if not new_status:
        raise ValueError("Statut requis")

    if new_status not in STATUS:
        raise ValueError(f"Statut invalide : {new_status}")

    order = get_order_by_id(session, order_id)
    order.statut = new_status

    session.commit()
    session.refresh(order)
    return order
