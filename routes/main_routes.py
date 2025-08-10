from flask import Blueprint

main_bp = Blueprint("main", __name__)


# Routes :
@main_bp.route("/")
def home():
    return "e-commerce API is operating"
