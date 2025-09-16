from flask import request, Blueprint, jsonify, g, Response
from app.core.auth_decorators import access_granted
from app.services.order_services import (
    get_all_orders, get_order_by_id, create_new_order,
    change_status_order, get_orderitems_all
    )
from app.core.exceptions.app_errors import ForbiddenError
from typing import Tuple, List

from app.schemas.order_schemas import (
    OrderCreateSchema, OrderUpdateSchema, OrderRespSchema, OrderItemRespSchema,
    OrderListSchema, OrderCreateRespSchema, OrderUpdateRespSchema
)
from pydantic import ValidationError
from app.schemas.errors.order_errors import(
    OrderCreateError, OrderUpdateError, OrderListError, OrderGetError
)
from spectree import Response as SpecResp
from app.spec import spec

order_bp = Blueprint("order_bp", __name__)


# GET /api/commandes
@order_bp.route("", methods=["GET"])
@access_granted('admin', 'client')
@spec.validate(resp=SpecResp(HTTP_200=OrderListSchema, HTTP_422=OrderListError), tags=["Commandes"])
def list_orders() -> Tuple[Response, int]:
    """
    Récupère toutes les commandes (admin) ou celles du client.
    """
    orders = get_all_orders(g.session, user=g.current_user)
    response = [OrderRespSchema.model_validate(o).model_dump() for o in orders]
    return jsonify(response), 200


# GET /api/commandes/<id>
@order_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
@spec.validate(resp=SpecResp(HTTP_200=OrderRespSchema, HTTP_422=OrderGetError), tags=["Commandes"])
def get_order_id(id: int) -> Tuple[Response, int]:
    """
    Récupère les détails d'une commande (admin, client propriétaire).
    Lève une erreur ForbiddenError si utilisateur non autorisé
    """
    order = get_order_by_id(g.session, id)
    if (g.current_user.role != "admin"
            and order.utilisateur_id != g.current_user.id):
        raise ForbiddenError("Accès refusé")

    response = OrderRespSchema.model_validate(order)
    return jsonify(response), 200


# POST /api/commandes
@order_bp.route("", methods=["POST"])
@access_granted('client')
@spec.validate(json=OrderCreateSchema,
               resp=SpecResp(HTTP_201=OrderCreateRespSchema, HTTP_422=OrderCreateError),
               tags=["Commandes"])
def create_order() -> Tuple[Response, int]:
    """
    Création d'une commande pour un client (client uniquement).
    Lève une erreur BadRequestError :
        si chanmp adresse_livraison vide
        si aucun champ produits
    """   
    body = OrderCreateSchema.model_validate(request.json)
    body = body.model_dump(exclude_none=True)
    order = create_new_order(
        g.session,
        user_id=g.current_user.id,
        items=body["produits"],
        address=body["adresse_livraison"]
    )

    response_items = [
        OrderItemRespSchema.model_validate(item).model_dump()
        for item in order.items
        ]

    commande_response = {**order.to_dict(), "lignes": response_items}

    return jsonify({"message": f"Commande id:{order.id} créée", "commande": commande_response}), 201


# PATCH /api/commandes/<id>
@order_bp.route("/<int:id>", methods=["PATCH"])
@access_granted('admin')
@spec.validate(json=OrderUpdateSchema,
               resp=SpecResp(HTTP_200=OrderUpdateRespSchema, HTTP_422=OrderUpdateError),
               tags=["Commandes"])
def update_status_order(id: int) -> Tuple[Response, int]:
    """
    Modifie le statut d'une commande (admin uniquement).
    Lève une erreur BadRequestError si statut invalide
    """
    try:
        body = OrderUpdateSchema.model_validate(request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422
    
    order = change_status_order(g.session, id, body.statut)
    response = {"id": order.id, "statut": order.statut}
    return jsonify({"message": "Statut mis à jour", "commande": response}), 200


# GET /api/commandes/<id>/lignes
@order_bp.route("/<int:id>/lignes", methods=["GET"])
@spec.validate(resp=SpecResp(HTTP_200=List[OrderItemRespSchema], HTTP_422=OrderListError), tags=["Commandes"])
def list_orderitems(id: int) -> Tuple[Response, int]:
    """
    Récupère les lignes d'une commande (accès public !!).
    """
    order = get_order_by_id(g.session, id)
    items = get_orderitems_all(g.session, order.id)

    result = [item.to_dict() for item in items]
    return jsonify(result), 200
