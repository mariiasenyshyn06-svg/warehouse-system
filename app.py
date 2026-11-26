import os

from flask import Flask, jsonify

from config import Config
from database import db


def create_app(config_class=Config):
    """Створює та налаштовує Flask-застосунок."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)
    db.init_app(app)

    import models  # noqa: F401  (щоб SQLAlchemy "побачив" усі таблиці)

    with app.app_context():
        db.create_all()

    @app.route("/")
    def index():
        return "Система складського обліку працює!"

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5001)