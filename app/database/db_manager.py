from app.database.base import Base, engine
import os


class DatabaseManager:
    """ Gestion création/suppression des tables SQLAlchemy. """

    def __init__(self, base=Base, engine=engine):
        self.base = base
        self.engine = engine
        self.env = os.getenv("FLASK_ENV", "dev")

    def init_db(self) -> None:
        """Crée toutes les tables selon les modèles SQLAlchemy."""
        if self.env != "prod":
            self.base.metadata.create_all(bind=self.engine)
        else:
            raise RuntimeError("Création de tables interdite en PROD !")

    def close_db(self) -> None:
        """Supprime toutes les tables définies dans les modèles SQLAlchemy."""
        if self.env != "prod" and self.env != "dev":
            self.base.metadata.drop_all(bind=self.engine)
        else:
            raise RuntimeError("Suppression de tables interdite en PROD !")