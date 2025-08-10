from flask import Flask
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.test_routes import test_bp


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(test_bp, url_prefix="/api")
    # app.register_blueprint(main_bp, url_prefix="/api/xxx")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
