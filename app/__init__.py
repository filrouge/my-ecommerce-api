from flask import Flask
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from app.routes.order_routes import order_bp

from app.database.sessions import init_session
from app.core.errors_handlers import register_error_handlers
from flask.app import Flask as FlaskType

import os
from config import CONFIG_MAP
from app.database.db_manager import DatabaseManager


def create_app() -> FlaskType:
    '''
    Point d'entrée de la Factory Flask assurant :
        - l'enregistrement des routes via Blueprints
        - la creation des tables si inexistantes -> migré vers init_db.py
        - l'intégration des exceptions handlers
    '''
    # Config selon export FLASK_ENV
    ENV = os.getenv("FLASK_ENV", "dev").lower()
    app_config = CONFIG_MAP.get(ENV, CONFIG_MAP["dev"])

    app = Flask(__name__)
    app.config.from_object(app_config)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/produits")
    app.register_blueprint(order_bp, url_prefix="/api/commandes")

    db_manager = DatabaseManager()
    db_manager.init_db()

    if ENV not in ("testing", "test"):
        init_session(app)

    register_error_handlers(app)

    return app

