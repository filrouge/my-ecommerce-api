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
from app.schemas.errors.validation_schemas import ValidationErrorsSchema
from app.schemas.product_schemas import (
    ProductCreateSchema, ProductUpdateSchema, ProductRespSchema,
    ProductCreateRespSchema, ProductUpdateRespSchema,
    ProductDeleteRespSchema, ProductListSchema)
from app.schemas.errors.product_errors import (
    ProductCreateError, ProductUpdateError, ProductDeleteError,
    ProductListError)

product_bp = Blueprint("product_bp", __name__)

# GET /api/produits
@product_bp.route("", methods=["GET"])
@spec.validate(resp=SpecResp(HTTP_200=ProductListSchema, HTTP_422=ProductListError), tags=["Produits"])
def get_products() -> Tuple[Response, int]:
    """
    Récupère la liste complète des produits en base (JSON).

    Retourne une erreur pour toute erreur base
    """
    products = get_all_products(g.session)

    # result = [product.to_dict() for product in products]
    result = [ProductRespSchema.model_validate(p).model_dump() for p in products]
    return jsonify(result), 200


# GET /api/produits/search
@product_bp.route("/search", methods=["GET"])
@spec.validate(resp=SpecResp(HTTP_200=ProductListSchema, HTTP_422=ProductListError), tags=["Produits"])
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
@spec.validate(resp=SpecResp(HTTP_200=ProductRespSchema, HTTP_422=ValidationErrorsSchema), tags=["Produits"])
def get_product(id: int) -> Tuple[Response, int]:
    """
    Récupère un produit par son ID (JSON).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
    """
    product = get_product_id(g.session, id)
    response = ProductRespSchema.model_validate(product)
    return jsonify(response.model_dump()), 200


# POST /api/produits
@product_bp.route('', methods=['POST'])
@access_granted('admin')
@spec.validate(json=ProductCreateSchema, resp=SpecResp(HTTP_201=ProductCreateRespSchema, HTTP_422=ProductCreateError), tags=["Produits"])
def create_product() -> Tuple[Response, int]:
    """
    Création d'un nouveau produit (admin uniquement).

    Retourne une erreur :
        si JSON invalide
        pour toute erreur base
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
@spec.validate(json=ProductUpdateSchema, resp=SpecResp(HTTP_200=ProductUpdateRespSchema, HTTP_422=ProductUpdateError), tags=["Produits"])
def update_product_id(id: int) -> Tuple[Response, int]:
    """
    Mise à jour des caractéristiques d'un produit (admin uniquement).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
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
@spec.validate(resp=SpecResp(HTTP_200=ProductDeleteRespSchema, HTTP_422=ProductDeleteError), tags=["Produits"])
def delete_product(id: int) -> Tuple[Response, int]:
    """
    Supprime un produit du catalogue (admin uniquement).

    Retourne une erreur :
        si produit introuvable
        pour toute erreur base
    """
    delete_product_id(g.session, id)
    return jsonify({"message": f"Produit {id} supprimé", "deleted_id": id}), 200
    # return jsonify({"message": f"Produit {id} supprimé"}), 200
