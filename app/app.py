from flask import Flask
from app.routes.main_routes import main_bp
from app.routes.auth_routes import auth_bp
from app.routes.product_routes import product_bp
from app.routes.order_routes import order_bp

from app.model.database import Base, engine
from app.model.sessions import init_session
from app.core.errors_handlers import register_error_handlers

from flask.app import Flask as FlaskType
from .config import Config

import os
from .config import Config, TestConfig, DevConfig, ProdConfig


def create_app() -> FlaskType:
    '''
    Point d'entrée de la Factory Flask assurant :
        - l'enregistrement des routes via Blueprints
        - la creation des tables si inexistantes
        - l'intégration des exceptions handlers
    '''

    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/produits")
    app.register_blueprint(order_bp, url_prefix="/api/commandes")

    Base.metadata.create_all(bind=engine)

    init_session(app)
    register_error_handlers(app)

    return app


env = os.getenv("FLASK_ENV", "dev").lower()
if env == "testing":
    config_class = TestConfig
elif env == "prod":
    config_class = ProdConfig
else:
    config_class = DevConfig

app = create_app()
app.config.from_object(config_class)


if __name__ == "__main__":
    app.run(debug=True)
