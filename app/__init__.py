from flask import Flask, jsonify
from flask_cors import CORS

from app.database import init_db
from app.routes import pages_bp, api_bp


def create_app():

    app = Flask(__name__)

    # Ayarlar
    app.config["SECRET_KEY"] = "nexovia-secret-key"
    app.config["DATABASE_URL"] = "nexovia.db"

    # CORS
    CORS(app)

    # Veritabanını başlat
    init_db(app)

    # Sayfa rotaları
    app.register_blueprint(pages_bp)

    # API rotaları
    app.register_blueprint(
        api_bp,
        url_prefix="/api"
    )

    # Sağlık kontrolü
    @app.route("/health")
    def health():
        return jsonify({
            "basari": True,
            "durum": "aktif",
            "proje": "Nexovia SmartLead AI"
        })

    return app