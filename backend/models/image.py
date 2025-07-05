from app import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = "image"

    id              = db.Column(db.Integer, primary_key=True)
    filename        = db.Column(db.String(120), nullable=False)
    date_upload     = db.Column(db.DateTime, default=datetime.utcnow)
    annotation      = db.Column(db.String(10), nullable=False)
    annotation_auto = db.Column(db.String(10), nullable=True)
    # Nouveaux champs Sprint 2
    taille          = db.Column(db.Integer)
    largeur         = db.Column(db.Integer)
    hauteur         = db.Column(db.Integer)
    contraste       = db.Column(db.Float)
    couleur_moyenne = db.Column(db.String(20))
    metadata_json   = db.Column(db.JSON)

