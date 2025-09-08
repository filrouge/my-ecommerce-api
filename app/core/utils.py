from app.core.errors_handlers import BadRequestError
from flask import Request


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

STATUS = ["En attente", "Validée", "Expédiée", "Annulée"]


def get_json_body(request: Request) -> dict:
    """
    Vérifie la validité du JSON d'entrée et le renvoie.

    Lève une erreur si JSON absent ou invalide.
    """
    if not (body := request.get_json()) or not isinstance(body, dict):
        raise BadRequestError("JSON invalide")

    return body


def forbidden_fields(body: dict, fields: dict) -> None:
    """
    Vérifie qu'aucun champ non autorisé n'est présent dans body.
    
    Lève une erreur au moins un champ non autorisé dans body.
    """
    forbidden = [field for field in body if field not in fields]
    if forbidden:
        raise BadRequestError(f"Champ(s) interdit(s): {', '.join(forbidden)}")


def required_fields(body: dict, fields: dict, optional_fields: set[str] = None) -> None:
    """
    Vérifie et valide la présence de champs obligatoires.

    Lève une erreur si un seul des champs est manquant.
    """
    forbidden_fields(body, fields)

    optional_fields = set() if optional_fields is None else set(optional_fields)
    if optional_fields == set(fields):
        raise BadRequestError("Aucun champ")

    required = set(fields) - optional_fields
    missing = [field for field in required if field not in body]
    if missing:
        raise BadRequestError(f"Champ(s) manquant(s) : {', '.join(missing)}")

    return True


def check_valid_fields(body: dict, fields: dict) -> None:
    """
    Vérifie la validité d'un champ selon le type et la valeur attendus.

    Lève une erreur si champ vide, type incorrect ou valeur négative.
    """
    for field, typ in fields.items():
        if field not in body:
            continue

        value = body[field]

        if value in (None, '', [], {}):
            raise BadRequestError(f"Champ {field} est vide")

        if not isinstance(value, typ):
            expected_type = typ.__name__ if not isinstance(typ, tuple) else " ou ".join(t.__name__ for t in typ)

            raise BadRequestError(
                f"Champ {field} invalide: type {expected_type} attendu"
                )

        if isinstance(value, (int, float)) and value < 0:
            raise BadRequestError(f"Champ {field} invalide: valeur négative")


def validate_json_fields(body: dict, fields: dict, optional_fields: set[str] = None) -> bool:
    """
    Valide le body JSON en vérifiant les clés et les champs.

    Lève une erreur si aucun champ attendu.
    """
    required_fields(body, fields, optional_fields)

    if not any(k in fields for k in body):
        raise BadRequestError("Aucune donnée valide")

    check_valid_fields(body, fields)

    return True
