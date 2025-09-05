from core.errors_handlers import BadRequestError

USER_FIELDS = {
    "email": str,
    "nom": str,
    "password": str,
    "role": str
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


def filter_valid_fields(body, allowed_fields):
    """ Vérifie l'absence de champs interdits et filtre sur ceux autorisés. """
    forbidden = set(body) - set(allowed_fields)
    if forbidden:
        raise BadRequestError(f"Champ(s) {next(iter(forbidden))} interdit(s)")

    filtered = {k: v for k, v in body.items() if k in allowed_fields}
    if not filtered:
        raise BadRequestError("Aucune donnée valide")

    return filtered


def check_valid_fields(field, value, expected_type):
    """ Vérifie l'absence de champs vides, de type incorrect ou négatifs. """
    if value in (None, '', [], {}):
        raise BadRequestError(f"Champ {field} est vide")

    if not isinstance(value, expected_type):
        raise BadRequestError(f"Champ {field} invalide: type {expected_type} attendu")

    if isinstance(value, (int, float)) and value < 0:
        raise BadRequestError(f"Champ {field} invalide: valeur négative")


def validate_json_fields(body: dict, allowed_fields: dict) -> bool:
    filtered = filter_valid_fields(body, allowed_fields)

    for field, expected_type in allowed_fields.items():
        if field in filtered:
            check_valid_fields(field, filtered[field], expected_type)

    return True
