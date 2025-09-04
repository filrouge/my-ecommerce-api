from core.errors_handlers import BadRequestError

USER_FIELDS = ["email", "password", "nom", "role"]
PRODUCT_FIELDS = ["nom", "description", "categorie", "prix", "quantite_stock"]
ORDER_FIELDS = ["utilisateur_id", "adresse_livraison", "statut", "date_commande"]
ORDERITEMS_FIELDS = ["commande_id", "produit_id", "quantite", "prix_unitaire"]

STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]


def get_json_body(request):
    """
    Récupère et valide le JSON d'entrée.
    Lève BadRequestError si JSON absent ou invalide.
    """
    if not (body := request.get_json()) or not isinstance(body, dict):
        raise BadRequestError("JSON invalide")
    return body


def required_fields(body, required_field):
    '''
    Vérifie et valide la présence des champs requis.
    Lève BadRequestError si un seul des champs est manquant.
    '''
    # Doublon avec get_json_body()
    # if not body:
    #     raise BadRequestError("JSON invalide")

    missing = [field for field in required_field if field not in body]
    if missing:
        raise BadRequestError(f"Champs manquant(s) : {', '.join(missing)}")

    return True
