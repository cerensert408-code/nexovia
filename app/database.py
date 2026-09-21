import sqlite3
from flask import current_app


def get_db():
    """
    SQLite veritabanına bağlanır.
    Satırlara sütun isimleriyle erişebilmek için Row kullanılır.
    """
    db = sqlite3.connect(current_app.config["DATABASE_URL"])
    db.row_factory = sqlite3.Row
    return db


def init_db(app):
    """
    Leads tablosunu oluşturur.
    Tablo daha önce oluşturulmuşsa tekrar oluşturulmaz.
    """
    with app.app_context():
        db = get_db()

        db.execute("""
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        db.commit()
        db.close()


def lead_ekle(isim, telefon, mesaj):
    """
    Yeni bir müşteri adayı kaydeder.
    SQL Injection'a karşı parametreli sorgu kullanılır.
    """
    db = get_db()

    try:
        db.execute(
            """
            INSERT INTO leads (isim, telefon, mesaj)
            VALUES (?, ?, ?)
            """,
            (isim, telefon, mesaj)
        )

        db.commit()

    finally:
        db.close()


def tum_leadler():
    """
    Tüm lead kayıtlarını en yeniden eskiye getirir.
    """
    db = get_db()

    try:
        leads = db.execute(
            """
            SELECT id, isim, telefon, mesaj, tarih
            FROM leads
            ORDER BY tarih DESC
            """
        ).fetchall()

        return [dict(lead) for lead in leads]

    finally:
        db.close()