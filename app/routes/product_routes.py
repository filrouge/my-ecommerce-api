from flask import request, jsonify, Blueprint, g, Response
from app.services.product_services import (
    get_all_products, get_product_id, add_product,
    update_product, delete_product_id, search_product
)
from app.core.auth_decorators import access_granted
from typing import Tuple

from spectree import Response as SpecResp
from app.spec import spec
from pydantic import ValidationError
from app.schemas.errors.json_schemas import ValidationErrorSchema
from app.schemas.product_schemas import (
    ProductCreateSchema, ProductUpdateSchema, ProductRespSchema,
    ProductCreateRespSchema, ProductUpdateRespSchema,
    ProductDeleteRespSchema, ProductListSchema)
from app.schemas.errors.product_errors import (
    ProductCreateError, ProductUpdateError, ProductDeleteError, ProductListError,
    ProductError400, ProductError401, ProductError403, ProductError404
)

product_bp = Blueprint("product_bp", __name__)


# GET /api/produits
@product_bp.route("", methods=["GET"])
@spec.validate(
    resp=SpecResp(HTTP_200=ProductListSchema, HTTP_422=ProductListError,
                  HTTP_400=ProductError400, HTTP_401=ProductError401,
                  HTTP_403=ProductError403,HTTP_404=ProductError404),
    tags=["Produits"]
)
def get_products() -> Tuple[Response, int]:
    """
    Liste complète des produits du catalogue
    """
    products = get_all_products(g.session)

    # result = [product.to_dict() for product in products]
    result = [ProductRespSchema.model_validate(p).model_dump() for p in products]
    return jsonify(result), 200


# GET /api/produits/search
@product_bp.route("/search", methods=["GET"])
@spec.validate(
    resp=SpecResp(HTTP_200=ProductListSchema, HTTP_422=ProductListError,
                  HTTP_400=ProductError400, HTTP_401=ProductError401,
                  HTTP_403=ProductError403,HTTP_404=ProductError404),
    tags=["Produits"]
)
def list_products() -> Tuple[Response, int]:
    """
    Recherche de produits par nom, catégorie ou disponibilité
    """
    nom = request.args.get("nom")
    categorie = request.args.get("categorie")
    disponible = request.args.get("disponible", "false").lower() == "true"

    products = search_product(
        g.session,
        nom=nom,
        categorie=categorie,
        disponible=disponible
        ) if (nom or categorie or disponible) else get_all_products(g.session)

    # result = [product.to_dict() for product in products]
    result = [ProductRespSchema.model_validate(p).model_dump() for p in products]
    return jsonify(result), 200


# GET /api/produits/<id>
@product_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
@spec.validate(
    resp=SpecResp(HTTP_200=ProductRespSchema, HTTP_422=ValidationErrorSchema,
                  HTTP_400=ProductError400, HTTP_401=ProductError401,
                  HTTP_403=ProductError403,HTTP_404=ProductError404),
    tags=["Produits"]
)
def get_product(id: int) -> Tuple[Response, int]:
    """
    Recherce de produit via son ID
    """
    product = get_product_id(g.session, id)
    response = ProductRespSchema.model_validate(product)
    return jsonify(response.model_dump()), 200


# POST /api/produits
@product_bp.route('', methods=['POST'])
@access_granted('admin')
@spec.validate(
    json=ProductCreateSchema,
    resp=SpecResp(HTTP_201=ProductCreateRespSchema, HTTP_422=ProductCreateError,
                  HTTP_400=ProductError400, HTTP_401=ProductError401,
                  HTTP_403=ProductError403,HTTP_404=ProductError404),
    tags=["Produits"]
)
def create_product() -> Tuple[Response, int]:
    """
    Ajout de produit au catalogue (admin only).
    """
    try:
        body = ProductCreateSchema(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422

    body = body.model_dump()
    product = add_product(
        g.session,
        nom=body["nom"],
        description=body.get("description", ""),
        categorie=body.get("categorie", ""),
        prix=body.get("prix"),
        quantite_stock=body.get("quantite_stock", 0)
    )
    response = ProductRespSchema.model_validate(product)
    return jsonify({
        "message": "Produit ajouté",
        "produit": response.model_dump()
        }), 201


# PUT /api/produits/<id>
@product_bp.route("/<int:id>", methods=["PUT"])
@access_granted('admin')
@spec.validate(
    json=ProductUpdateSchema,
    resp=SpecResp(HTTP_200=ProductUpdateRespSchema, HTTP_422=ProductUpdateError,
                  HTTP_400=ProductError400, HTTP_401=ProductError401,
                  HTTP_403=ProductError403,HTTP_404=ProductError404),
    tags=["Produits"]
)
def update_product_id(id: int) -> Tuple[Response, int]:
    """
    Mise à jour des caractéristiques produit (admin only)
    """
    try:
        body = ProductUpdateSchema(**request.json)
    except ValidationError as e:
        return jsonify({"errors": e.errors()}), 422
    
    body = body.model_dump(exclude_none=True)
    product = update_product(g.session, id, **body)
    response = ProductRespSchema.model_validate(product)
    return jsonify(
        {
            "message": "Produit mis à jour",
            "produit_id": product.id,
            "produit": response.model_dump()
        }
    ), 200


# DELETE /api/produits/<id>
@product_bp.route("/<int:id>", methods=["DELETE"])
@access_granted('admin')
@spec.validate(
    resp=SpecResp(HTTP_200=ProductDeleteRespSchema, HTTP_422=ProductDeleteError,
                  HTTP_400=ProductError400, HTTP_401=ProductError401,
                  HTTP_403=ProductError403,HTTP_404=ProductError404),
    tags=["Produits"]
)
def delete_product(id: int) -> Tuple[Response, int]:
    """
    Suppression de produit du catalogue (admin only)
    """
    delete_product_id(g.session, id)
    return jsonify({"message": f"Produit {id} supprimé", "deleted_id": id}), 200
    # return jsonify({"message": f"Produit {id} supprimé"}), 200
