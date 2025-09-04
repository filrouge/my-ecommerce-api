from core.errors_handlers import BadRequestError

REGISTER_FIELDS = {
    "email": str,
    "nom": str,
    "password": str
}
PRODUCT_FIELDS = {
    "nom": str,
    "description": str,
    "categorie": str,
    "prix": (int, float),
    "quantite_stock": (int)
}
ORDER_FIELDS = {
    "produits": list,
    "adresse_livraison": str,
    "statut": str
}
ORDER_ITEM_FIELDS = {
    "produit_id": (int),
    "quantite": (int),
}
NUMERIC_FIELDS = {
    "prix": (int, float),
    "quantite_stock": (int),
    "quantite": (int),
}

STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]


def get_json_body(request):
    """
    Récupère et valide le JSON d'entrée.
    Lève BadRequestError si JSON absent ou invalide.
    """
    if not (body := request.get_json()) or not isinstance(body, dict):
        raise BadRequestError("JSON invalide")
    return body


def required_fields(body: dict, required_fields: dict) -> bool:
    """
    Vérifie que tous les champs obligatoires sont présents.
    """
    missing = [field for field in required_fields if field not in body]
    if missing:
        raise BadRequestError(f"Champs manquant(s) : {', '.join(missing)}")

    return True
