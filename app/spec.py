from spectree import SpecTree
from spectree.models import SecurityScheme


# Initialisation de l'instance Spectree
spec = SpecTree(
    "flask",
    title="My E-commerce API",
    version="1.0.0",
    description="Documentation API Flask (via Spectree)",

    servers=[{"url": "http://localhost:5000"}],
    # # Pour forcer Swagger UI à ne pas montrer "Servers" (-> plus de cURL tests)
    # servers=[],

    # Sécurité appliquée globalement
    security=[{"bearerAuth": []}],

    # Schéma de sécurité pour Swagger UI
    security_schemes=[
        SecurityScheme(
            name="auth_TOKEN",
            data={"type": "apiKey", "name": "Authorization", "in": "header"},
        )]
)
