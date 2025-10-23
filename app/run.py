# import os
from app import create_app


if __name__ == "__main__":
    # debug = os.getenv("FLASK_ENV", "dev") == "dev"
    app = create_app()
    app.run(debug=True)
    # app.run(host="127.0.0.1", port=5000, debug=debug)
