from sqlalchemy.exc import (
    IntegrityError,
    OperationalError,
    DataError,
    StatementError
)
from typing import Type, Dict, Tuple


# Mapping des exceptions ORM
ORM_ERROR_MAP: Dict[Type[Exception], Tuple[int, str]] = {
    IntegrityError: (409, "Contrainte d'intégrité violée"),
    OperationalError: (503, "Service database indisponible"),
    DataError: (400, "Donnée invalide ou contrainte violée"),
    StatementError: (500, "Erreur dans la requête SQL"),
    RuntimeError: (409, "Conflit d'état / ressource")
}
