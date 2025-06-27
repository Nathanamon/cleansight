# backend/routes/images.py

from flask import Blueprint, jsonify
from app import db
from models.image import Image

images_bp = Blueprint("images", __name__)

@images_bp.route("/images", methods=["GET"])
def get_images():
    images = Image.query.order_by(Image.id.asc()).all()
    data = [{
        "id":          img.id,
        "filename":    img.filename,
        "date_upload": img.date_upload.isoformat(),
        "annotation":  img.annotation,
        "largeur":     img.largeur,
        "hauteur":     img.hauteur,
        "taille":      img.taille
    } for img in images]
    return jsonify(data), 200
