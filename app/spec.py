from spectree import SpecTree

spec = SpecTree(
    "flask",
    title="My E-commerce API",
    version="1.0.0",
    description="Documentation API Flask (via Spectree)",
    servers=[{"url": "http://localhost:5000"}],
    # Force pour que Swagger UI ne montre pas de "Servers"
    # Sans "Servers" -> perte de la possibilité de cURL tests
    # servers=[],
)
