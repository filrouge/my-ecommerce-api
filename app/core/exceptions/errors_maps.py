# Mapping des exceptions Applicatives et ORM (doc Swagger)

APP_ERROR_MAP = {
    "order": {
        400: {"error": "Stock insuffisant"},
        401: {"error": "Accès refusé"},
        403: {"error": "Accès interdit"},
        404: {"error": "Commande introuvable"}
    },
    "orderitem": {
        400: {"error": "Stock insuffisant"},
        401: {"error": "Accès refusé"},
        403: {"error": "Accès interdit"},
        404: {"error": "Ligne de commande introuvable"}
    },
    "product": {
        400: {"error": "Produit introuvable"},
        401: {"error": "Accès refusé"},
        403: {"error": "Accès interdit"},
        404: {"error": "Produit introuvable"}
    },
    "user": {
        400: {"error": "Adresse e-mail déjà utilisée"},
        401: {"error": "Accès refusé "},
        403: {"error": "Identifiants invalides"},
        404: {"error": "Client introuvable "}
    },
    "global": {
        500: {"error": "Erreur Interne"}
    }
}

ORM_ERROR_MAP = {
    "IntegrityError": {
        409: {"error": "Contrainte d'intégrité violée"}
        },
    "OperationalError": {
        503: {"error": "Service database indisponible"}
        },
    "DataError": {
        400: {"error": "Donnée invalide ou contrainte violée"}
        },
    "StatementError": {
        500: {"error": "Erreur dans la requête SQL"}
        },
    "RuntimeError": {
        409: {"error": "Conflit d'état / ressource"}
        }
}
