from flask import Flask
from routes.main_routes import main_bp
from routes.auth_routes import auth_bp
from routes.test_routes import test_bp

from model.models import Base, engine, SessionLocal


def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(test_bp, url_prefix="/api")

    Base.metadata.create_all(bind=engine)

    return app


app = create_app()


# Ensure removal of session when ending request
@app.teardown_appcontext
def remove_session(exception=None):
    SessionLocal.remove()


if __name__ == "__main__":
    app.run(debug=True)
