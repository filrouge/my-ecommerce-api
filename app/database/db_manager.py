from app.database.base import Base, engine

class DatabaseManager:
    """
    Gestion de la création et suppression des tables SQLAlchemy.
    Peut être utilisé depuis la factory Flask ou les tests.
    """

    def __init__(self, base=Base, engine=engine):
        self.base = base
        self.engine = engine

    def init_db(self) -> None:
        """Crée toutes les tables selon les modèles SQLAlchemy."""
        self.base.metadata.create_all(bind=self.engine)

    def close_db(self) -> None:
        """Supprime toutes les tables définies dans les modèles SQLAlchemy."""
        self.base.metadata.drop_all(bind=self.engine)