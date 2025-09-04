from flask import request, jsonify, Blueprint, g
from core.auth_utils import required_fields
from services.product_utils import (
    get_all_products,
    get_product_id,
    add_product,
    update_product,
    delete_product_id,
    search_product
)
from core.auth import access_granted
from services.exceptions_utils import BadRequestError

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("", methods=["GET"])
def get_products():
    """ Liste tous les produits du catalogue. """
    products = get_all_products(g.session)

    result = [product.to_dict() for product in products]
    return jsonify(result), 200


@product_bp.route("/search", methods=["GET"])
def list_products():
    """ Liste les produits selon le nom, la catégorie ou la disponibilité. """
    nom = request.args.get("nom")
    categorie = request.args.get("categorie")
    disponible = request.args.get("disponible", "false").lower() == "true"

    if nom or categorie or disponible:
        products = search_product(
            g.session,
            nom=nom,
            categorie=categorie,
            disponible=disponible
            )
    else:
        products = get_all_products(g.session)

    result = [product.to_dict() for product in products]
    return jsonify(result), 200


@product_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
def get_product(id):
    """ Liste un produit selon son id. """
    product = get_product_id(g.session, id)
    return jsonify(product.to_dict()), 200


@product_bp.route('', methods=['POST'])
@access_granted('admin')
def create_product():
    """ Crée un produit avec ses caractéristiques. """
    body = request.json
    required_fields(
        body,
        ["nom", "description", "categorie", "prix", "quantite_stock"]
    )

    product = add_product(
        g.session,
        nom=body["nom"],
        description=body.get("description", ""),
        categorie=body.get("categorie", "Autre"),
        prix=body.get("prix", 0),
        quantite_stock=body.get("quantite_stock", 0)
    )
    return jsonify(
        {
            "message": "Produit ajouté",
            "produit": product.to_dict()
        }
    ), 201


@product_bp.route("/<int:id>", methods=["PUT"])
@access_granted('admin')
def update_product_id(id):
    """ Modifie des caractéristiques d'un produit selon son id. """
    if not (body := request.get_json()) or not isinstance(body, dict):
        raise BadRequestError("JSON invalide")

    allowed_fields = {
        "nom", "description", "categorie",
        "prix", "quantite_stock"
    }
    update_data = {k: v for k, v in body.items() if k in allowed_fields}

    if not update_data or not any(update_data.values()):
        raise BadRequestError("Aucune donnée valide pour la mise à jour")

    for field in ("prix", "quantite_stock"):
        if (value := body.get(field)) is not None and value < 0:
            raise BadRequestError(f"{field.capitalize()} invalide")

    product = update_product(g.session, id, **update_data)
    return jsonify(
        {
            "message": "Produit mis à jour",
            "produit_id": product.id,
            "produit": product.to_dict()
        }
    ), 200


@product_bp.route("/<int:id>", methods=["DELETE"])
@access_granted('admin')
def delete_product(id):
    """ Retire/Détruit du catalogue un produit selon son id. """
    delete_product_id(g.session, id)
    return jsonify({"message": f"Produit {id} supprimé"}), 200
