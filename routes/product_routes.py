from flask import request, jsonify, Blueprint
from model.sessions import get_session
from core.utils import required_fields
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
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
    session = get_session()
    try:
        products = get_all_products(session)
        result = [
            {
                "id": p.id,
                "nom": p.nom,
                "description": p.description,
                "categorie": p.categorie,
                "prix": p.prix,
                "quantite_stock": p.quantite_stock
            }
            for p in products
        ]
        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur Database: {str(e)}"}), 500


@product_bp.route("/search", methods=["GET"])
def list_products():
    """ Retourne la liste de produits par nom, catégorie ou disponibilité. """
    session = get_session()

    # Récupération des paramètres de la requête
    nom = request.args.get("nom")
    categorie = request.args.get("categorie")
    disponible = request.args.get("disponible", "false").lower() == "true"

    try:
        if nom or categorie or disponible:
            products = search_product(
                session,
                nom=nom,
                categorie=categorie,
                disponible=disponible
                )
        else:
            products = get_all_products(session)

        result = [
            {
                "id": product.id,
                "nom": product.nom,
                "description": product.description,
                "categorie": product.categorie,
                "prix": product.prix,
                "quantite_stock": product.quantite_stock
            }
            for product in products
        ]

        return jsonify(result), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": "Erreur Database", "details": str(e)}), 500


@product_bp.route("/<int:id>", methods=["GET"])
@access_granted('admin', 'client')
def get_product(id):
    session = get_session()
    try:
        product = get_product_id(session, id)
        return jsonify(product.to_dict()), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur Database: {str(e)}"}), 500


@product_bp.route('', methods=['POST'])
@access_granted('admin')
def create_product():
    data = request.json
    ok, error = required_fields(
        data,
        ["nom", "description", "categorie", "prix", "quantite_stock"]
        )

    session = get_session()

    try:
        product = add_product(
            session,
            nom=data["nom"],
            description=data.get("description", ""),
            categorie=data.get("categorie", "Autre"),
            prix=data.get("prix", 0),
            quantite_stock=data.get("quantite_stock", 0)
        )
        return jsonify(
            {
                "message": "Produit ajouté",
                "produit": product.to_dict()
            }
        ), 201

    except IntegrityError as e:
        return jsonify({"error": "Erreur Integrité", "details": str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": "Erreur Database", "details": str(e)}), 500


@product_bp.route("/<int:id>", methods=["PUT"])
@access_granted('admin')
def update_product_id(id):
    session = get_session()
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON non valide"}), 400

    try:
        product = update_product(session, id, **data)
        return jsonify(
            {
                "message": "Produit mis à jour",
                "produit_id": product.id,
                "produit": product.to_dict()
            }
        ), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except IntegrityError as e:
        return jsonify({"error": "Erreur Integrité", "details": str(e)}), 400
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur Database: {str(e)}"}), 500


@product_bp.route("/<int:id>", methods=["DELETE"])
@access_granted('admin')
def delete_product(id):
    session = get_session()
    try:
        delete_product_id(session, id)
        return jsonify({"message": f"Produit {id} supprimé"}), 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    except SQLAlchemyError as e:
        return jsonify({"error": f"Erreur Database: {str(e)}"}), 500
