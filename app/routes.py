from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler


# Sayfa rotaları
pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    return render_template("index.html")


# API rotaları
api_bp = Blueprint("api", __name__)


@api_bp.route("/leads", methods=["POST"])
def create_lead():
    data = request.get_json()

    if not data:
        return jsonify({
            "basari": False,
            "mesaj": "Veri gönderilmedi."
        }), 400

    isim = data.get("isim")
    telefon = data.get("telefon")
    mesaj = data.get("mesaj", "")

    if not isim or not telefon:
        return jsonify({
            "basari": False,
            "mesaj": "İsim ve telefon zorunludur."
        }), 400

    lead_ekle(isim, telefon, mesaj)

    return jsonify({
        "basari": True,
        "mesaj": "Lead başarıyla kaydedildi."
    }), 201


@api_bp.route("/leads", methods=["GET"])
def get_leads():
    leads = tum_leadler()

    return jsonify({
        "basari": True,
        "leadler": leads
    })