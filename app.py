from flask import Flask
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.to_test_routes import test_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp

from model.database import Base, engine
from model.sessions import init_session


def create_app():
    app = Flask(__name__)

    # Enregistrement des routes
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(test_bp, url_prefix="/api")
    app.register_blueprint(product_bp, url_prefix="/api/produits")
    app.register_blueprint(order_bp, url_prefix="/api/commandes")

    # Creation des tables si inexistantes
    Base.metadata.create_all(bind=engine)

    # Initialisation des sessions
    init_session(app)

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
