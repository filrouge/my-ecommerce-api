from flask import request, jsonify, Blueprint, g, Response
from app.services.product_utils import (
    get_all_products, get_product_id, add_product,
    update_product, delete_product_id, search_product
)
from app.core.permissions import access_granted
from app.core.utils import (
    get_json_body, validate_json_fields,
    PRODUCT_FIELDS,
    )
from typing import Tuple

product_bp = Blueprint("product_bp", __name__)


# GET /api/produits
@product_bp.route("", methods=["GET"])
def get_products() -> Tuple[Response, int]:
    """
    Récupère la liste complète des produits en base (JSON).

    Retourne une erreur :
        pour toute erreur base
    """
    products = get_all_products(g.session)

    result = [product.to_dict() for product in products]
    return jsonify(result), 200


# GET /api/produits/<id>
@product_bp.route("/search", methods=["GET"])
def list_products() -> Tuple[Response, int]:
    """
    Récupère la liste des produits selon les critères
    de nom, de catégorie ou de disponibilité (JSON).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
    """
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


# GET /api/produits/<id>
@product_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
def get_product(id: int) -> Tuple[Response, int]:
    """
    Récupère un produit par son ID (JSON).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
    """
    product = get_product_id(g.session, id)
    return jsonify(product.to_dict()), 200


# POST /api/produits
@product_bp.route('', methods=['POST'])
@access_granted('admin')
def create_product() -> Tuple[Response, int]:
    """
    Création d'un nouveau produit (admin uniquement).

    Retourne une erreur :
        si JSON invalide
        pour toute erreur base
    """
    body = get_json_body(request)

    # REQUIRED_FIELDS = {
    #     k: v for k, v in PRODUCT_FIELDS.items()
    #     if k not in {"description", "quantite_stock"}
    #     }
    # required_fields(body, REQUIRED_FIELDS)
    validate_json_fields(body, PRODUCT_FIELDS, {"description", "quantite_stock"})

    product = add_product(
        g.session,
        nom=body["nom"],
        description=body.get("description", ""),
        categorie=body.get("categorie", ""),
        prix=body.get("prix"),
        quantite_stock=body.get("quantite_stock", 0)
    )
    return jsonify(
        {
            "message": "Produit ajouté",
            "produit": product.to_dict()
        }
    ), 201


# PUT /api/produits/<id>
@product_bp.route("/<int:id>", methods=["PUT"])
@access_granted('admin')
def update_product_id(id: int) -> Tuple[Response, int]:
    """
    Mise à jour des caractéristiques d'un produit (admin uniquement).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
    """
    body = get_json_body(request)

    optional_fields = set(PRODUCT_FIELDS) - set(body.keys())
    validate_json_fields(body, PRODUCT_FIELDS, optional_fields)

    product = update_product(g.session, id, **body)
    return jsonify(
        {
            "message": "Produit mis à jour",
            "produit_id": product.id,
            "produit": product.to_dict()
        }
    ), 200


# DELETE /api/produits/<id>
@product_bp.route("/<int:id>", methods=["DELETE"])
@access_granted('admin')
def delete_product(id: int) -> Tuple[Response, int]:
    """
    Supprime un produit du catalogue (admin uniquement).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
    """
    delete_product_id(g.session, id)
    return jsonify({"message": f"Produit {id} supprimé"}), 200
