from datetime import datetime
from app import db  # attention au chemin selon ton projet

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    annotation = db.Column(db.String(10))
    taille = db.Column(db.Integer)
    largeur = db.Column(db.Integer)
    hauteur = db.Column(db.Integer)
    couleur_moyenne = db.Column(db.String(20))
