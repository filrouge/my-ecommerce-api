from flask import Blueprint, request, jsonify, g
from core.auth import access_granted
from services.order_utils import (
    get_all_orders,
    get_order_by_id,
    create_new_order,
    change_status_order,
    get_orderitems_all
)
from core.auth_utils import required_fields

order_bp = Blueprint("order_bp", __name__)


@order_bp.route("", methods=["GET"])
@access_granted('admin', 'client')
def list_orders():
    """ Liste toutes les commandes (admin) ou celles du client. """
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


@order_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
def get_order_id(id):
    """ Navigue sur une commande spécifique (admin, propriétaire). """
    current_user = g.current_user
    try:
        order = get_order_by_id(g.session, id)
        if (current_user.role != "admin"
                and order.utilisateur_id != current_user.id):
            return jsonify({"error": "Accès refusé"}), 403

        result = {
            "id": order.id,
            "utilisateur_id": order.utilisateur_id,
            "adresse_livraison": order.adresse_livraison,
            "statut": order.statut,
            "date_commande": str(order.date_commande)
        }
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@order_bp.route("", methods=["POST"])
@access_granted('client')
def create_order():
    """ Créer une commande client (+/- produit par ligne de commande) . """
    current_user = g.current_user
    # if current_user is None:
    #     return jsonify({"error": "Action Interdite"}), 401

    body = request.get_json()
    ok, error = required_fields(body, ["adresse_livraison", "produits"])
    if not ok:
        return jsonify({"error": str(error)}), 400

    try:
        order = create_new_order(
            g.session,
            user_id=current_user.id,
            items=body.get("produits", []),
            address=body.get("adresse_livraison")
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

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@order_bp.route("/<int:id>", methods=["PATCH"])
@access_granted('admin')
def update_status_order(id):
    """ Modifie le statut d'une commande spécifique (admin). """
    body = request.get_json()
    required_fields(body, ["statut"])

    new_status = body.get("statut")
    try:
        order = change_status_order(g.session, id, new_status)
        result = {
            "id": order.id,
            "statut": order.statut
        }
        return jsonify({
            "message": "Statut mis à jour",
            "commande": result
            }), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@order_bp.route("/<int:id>/lignes", methods=["GET"])
def list_orderitems(id):
    """ Navigue sur  les caractéristiques d'une ligne de commande spécifique
    (accès public !!). """
    try:
        order = get_order_by_id(g.session, id)
        items = get_orderitems_all(g.session, order.id)
        
        result = [item.to_dict() for item in items]
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
