# backend/models/image.py

from app import db
from datetime import datetime

class Image(db.Model):
    __tablename__ = "image"

    id          = db.Column(db.Integer, primary_key=True)
    filename    = db.Column(db.String(120), nullable=False)
    date_upload = db.Column(db.DateTime, default=datetime.utcnow)
    annotation  = db.Column(db.String(100), nullable=False)
    largeur     = db.Column(db.Integer)
    hauteur     = db.Column(db.Integer)
    taille      = db.Column(db.Integer)
