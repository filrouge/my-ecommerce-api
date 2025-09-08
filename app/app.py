from flask import Flask
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp

from model.database import Base, engine
from model.sessions import init_session
from core.errors_handlers import register_error_handlers

from flask.app import Flask as FlaskType


def create_app() -> FlaskType:
    '''
    Point d'entrée de la Factory Flask assurant :
        - l'enregistrement des routes via Blueprints
        - la creation des tables si inexistantes
        - l'intégration des exceptions handlers
    '''

    app = Flask(__name__)

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(product_bp, url_prefix="/api/produits")
    app.register_blueprint(order_bp, url_prefix="/api/commandes")

    Base.metadata.create_all(bind=engine)

    init_session(app)
    register_error_handlers(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
