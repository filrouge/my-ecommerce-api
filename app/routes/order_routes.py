from flask import request, Blueprint, jsonify, g, Response
from app.core.auth_decorators import access_granted
from app.services.order_services import (
    get_all_orders, get_order_by_id, create_new_order,
    change_status_order, get_orderitems_all
    )
from app.core.exceptions.app_errors import ForbiddenError, BadRequestError
from app.services.validators import (
    get_json_body, validate_json_fields,
    ORDER_FIELDS, ORDER_ITEM_FIELDS, STATUS
    )
from typing import Tuple

order_bp = Blueprint("order_bp", __name__)


# GET /api/commandes
@order_bp.route("", methods=["GET"])
@access_granted('admin', 'client')
def list_orders() -> Tuple[Response, int]:
    """
    Récupère toutes les commandes (admin) ou celles du client.
    """
    orders = get_all_orders(g.session, user=g.current_user)
    result = [{
        "id": order.id,
        "utilisateur_id": order.utilisateur_id,
        "adresse_livraison": order.adresse_livraison,
        "statut": order.statut,
        "date_commande": order.date_commande.isoformat()
    } for order in orders]
    # result = [order.to_dict() for order in orders]
    return jsonify(result), 200


# GET /api/commandes/<id>
@order_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
def get_order_id(id: int) -> Tuple[Response, int]:
    """
    Récupère les détails d'une commande (admin, client propriétaire).

    Lève une erreur ForbiddenError si utilisateur non autorisé
    """
    order = get_order_by_id(g.session, id)
    if (g.current_user.role != "admin"
            and order.utilisateur_id != g.current_user.id):
        raise ForbiddenError("Accès refusé")

    result = {
        "id": order.id,
        "utilisateur_id": order.utilisateur_id,
        "adresse_livraison": order.adresse_livraison,
        "statut": order.statut,
        "date_commande": str(order.date_commande)
    }
    return jsonify(result), 200


# POST /api/commandes
@order_bp.route("", methods=["POST"])
@access_granted('client')
def create_order() -> Tuple[Response, int]:
    """
    Création d'une commande pour un client (client uniquement).

    Lève une erreur BadRequestError :
        si chanmp adresse_livraison vide
        si aucun champ produits
    """
    body = get_json_body(request)
    validate_json_fields(body, ORDER_FIELDS, {"statut"})
    address = body["adresse_livraison"]

    items = body["produits"]
    for item in items:
        validate_json_fields(item, ORDER_ITEM_FIELDS)

    order = create_new_order(
        g.session,
        user_id=g.current_user.id,
        items=items,
        address=address
    )
    return jsonify(
        {
            "message": f"Commande id:{order.id} créée",
            "commande": order.to_dict()
            # "commande": {
            #     **order.to_dict(),
            #     "items": [item.to_dict() for item in order.items]
            #     }
        }
    ), 201


# PATCH /api/commandes/<id>
@order_bp.route("/<int:id>", methods=["PATCH"])
@access_granted('admin')
def update_status_order(id: int) -> Tuple[Response, int]:
    """
    Modifie le statut d'une commande (admin uniquement).

    Lève une erreur BadRequestError si statut invalide
    """
    body = get_json_body(request)
    validate_json_fields(body, ORDER_FIELDS, {"produits", "adresse_livraison"})

    new_status = body["statut"]
    if new_status not in STATUS:
        raise BadRequestError(f"Statut invalide : {new_status}")

    order = change_status_order(g.session, id, new_status)
    result = {
        "id": order.id,
        "statut": order.statut
    }
    return jsonify({
        "message": "Statut mis à jour",
        "commande": result
        }), 200


# GET /api/commandes/<id>/lignes
@order_bp.route("/<int:id>/lignes", methods=["GET"])
def list_orderitems(id: int) -> Tuple[Response, int]:
    """
    Récupère les lignes d'une commande (accès public !!).
    """
    order = get_order_by_id(g.session, id)
    items = get_orderitems_all(g.session, order.id)

    result = [item.to_dict() for item in items]
    return jsonify(result), 200
