from flask import Blueprint, request, jsonify, render_template
from app.database import lead_ekle, tum_leadler

# ==========================================
# SAYFA ROTALARI
# ==========================================

pages_bp = Blueprint("pages", __name__)


@pages_bp.route("/")
def home():
    return render_template("index.html")


# ==========================================
# API ROTALARI
# ==========================================

api_bp = Blueprint("api", __name__)


# ------------------------------------------
# YENİ LEAD EKLE
# ------------------------------------------

@api_bp.route("/leads", methods=["POST"])
def create_lead():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "basari": False,
            "mesaj": "Veri gönderilmedi."
        }), 400

    # Wix'ten gelecek bilgiler
    isim = data.get("isim", "").strip()
    telefon = data.get("telefon", "").strip()
    mesaj = data.get("mesaj", "").strip()

    # İsim ve telefon zorunlu
    if not isim:
        return jsonify({
            "basari": False,
            "mesaj": "İsim alanı zorunludur."
        }), 400

    if not telefon:
        return jsonify({
            "basari": False,
            "mesaj": "Telefon alanı zorunludur."
        }), 400

    # Veritabanına kaydet
    lead_ekle(
        isim,
        telefon,
        mesaj
    )

    return jsonify({
        "basari": True,
        "mesaj": "Bilgiler başarıyla kaydedildi.",
        "lead": {
            "isim": isim,
            "telefon": telefon,
            "mesaj": mesaj
        }
    }), 201


# ------------------------------------------
# TÜM LEADLERİ GETİR
# ------------------------------------------

@api_bp.route("/leads", methods=["GET"])
def get_leads():

    leads = tum_leadler()

    return jsonify({
        "basari": True,
        "leadler": leads
    })