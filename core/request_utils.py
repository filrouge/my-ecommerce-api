from core.errors_handlers import BadRequestError
from flask import Request
from typing import Any

USER_FIELDS: dict[str, type] = {
    "email": str,
    "nom": str,
    "password": str,
    "role": str
}
PRODUCT_FIELDS: dict[str, type | tuple[type, ...]] = {
    "nom": str,
    "description": str,
    "categorie": str,
    "prix": (int, float),
    "quantite_stock": (int)
}
ORDER_FIELDS: dict[str, type] = {
    "produits": list,
    "adresse_livraison": str,
    "statut": str
}
ORDER_ITEM_FIELDS: dict[str, type] = {
    "produit_id": (int),
    "quantite": (int),
}
NUMERIC_FIELDS: dict[str, type | tuple[type, ...]] = {
    "prix": (int, float),
    "quantite_stock": (int),
    "quantite": (int),
}

STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]


def get_json_body(request: Request) -> dict:
    """
    Vérifie la validité du JSON d'entrée et le renvoie.

    Lève une erreur si JSON absent ou invalide.
    """
    if not (body := request.get_json()) or not isinstance(body, dict):
        raise BadRequestError("JSON invalide")

    return body


def required_fields(body: dict, required_fields: dict) -> bool:
    """
    Vérifie et valide la présence de champs obligatoires.

    Lève une erreur si un seul des champs est manquant.
    """
    missing = [field for field in required_fields if field not in body]
    if missing:
        raise BadRequestError(f"Champs manquant(s) : {', '.join(missing)}")

    return True


def filter_valid_fields(body: dict, allowed_fields: dict) -> dict:
    """
    Vérifie la présence de champs interdits et filtre les champs autorisés.

    Lève une erreur si aucun champ attendu ou un des champs est inconnu.
    """
    forbidden = set(body) - set(allowed_fields)
    if forbidden:
        raise BadRequestError(f"Champ(s) {next(iter(forbidden))} interdit(s)")

    filtered = {k: v for k, v in body.items() if k in allowed_fields}
    if not filtered:
        raise BadRequestError("Aucune donnée valide")

    return filtered


def check_valid_fields(field: str, value: Any,
                       expected_type: type | tuple[type, ...]) -> None:
    """
    Vérifie la validité d'un champ selon le type et la valeur attendus.

    Lève une erreur si champ vide, type incorrect ou valeur négative.
    """
    if value in (None, '', [], {}):
        raise BadRequestError(f"Champ {field} est vide")

    if not isinstance(value, expected_type):
        raise BadRequestError(
            f"Champ {field} invalide: type {expected_type} attendu"
            )

    if isinstance(value, (int, float)) and value < 0:
        raise BadRequestError(f"Champ {field} invalide: valeur négative")


def validate_json_fields(body: dict, allowed_fields: dict) -> bool:
    """
    Valide le body JSON en vérfiant les clés et les champs.
    """
    filtered = filter_valid_fields(body, allowed_fields)

    for field, expected_type in allowed_fields.items():
        if field in filtered:
            check_valid_fields(field, filtered[field], expected_type)

    return True
