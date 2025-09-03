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

product_bp = Blueprint("product_bp", __name__)


@product_bp.route("", methods=["GET"])
def get_products():
    """ Liste tous les produits du catalogue. """
    try:
        products = get_all_products(g.session)
        result = [product.to_dict() for product in products]
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route("/search", methods=["GET"])
def list_products():
    """ Liste les produits selon le nom, la catégorie ou la disponibilité. """
    nom = request.args.get("nom")
    categorie = request.args.get("categorie")
    disponible = request.args.get("disponible", "false").lower() == "true"

    try:
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

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
def get_product(id):
    """ Liste un produit selon son id. """
    try:
        product = get_product_id(g.session, id)
        return jsonify(product.to_dict()), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route('', methods=['POST'])
@access_granted('admin')
def create_product():
    """ Crée un produit avec ses caractéristiques. """
    body = request.json
    ok, error = required_fields(
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
    body = request.get_json()
    if not body:
        return jsonify({"error": "JSON non valide"}), 400

    try:
        product = update_product(g.session, id, **body)
        return jsonify(
            {
                "message": "Produit mis à jour",
                "produit_id": product.id,
                "produit": product.to_dict()
            }
        ), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404


@product_bp.route("/<int:id>", methods=["DELETE"])
@access_granted('admin')
def delete_product(id):
    """ Retire/Détruit du catalogue un produit selon son id. """
    try:
        delete_product_id(g.session, id)
        return jsonify({"message": f"Produit {id} supprimé"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
