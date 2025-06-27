from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from cleansight.backend.models.image import db  # à adapter selon l’arborescence exacte

app = Flask(__name__)
app.config.from_pyfile('../../.env', silent=True)  # ou adapte si tu utilises config.py

with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès.")
