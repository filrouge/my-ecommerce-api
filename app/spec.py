from spectree import SpecTree

spec = SpecTree(
    "flask",
    title="My E-commerce API",
    version="1.0.0",
    description="Documentation API Flask (via Spectree)",
    servers=[{"url": "http://localhost:5000"}],
    # servers=[],  # Force pour que Swagger UI ne montre pas de "Servers"
)
