"""Flask web application for Steganox."""

import os

from flask import Flask

from steganox.ui.web.routes import register_routes


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB
    app.config["UPLOAD_FOLDER"] = os.path.join(os.getcwd(), "uploads")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", os.urandom(32))

    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    register_routes(app)
    return app


if __name__ == "__main__":
    create_app().run(debug=False, host="0.0.0.0", port=5000)
