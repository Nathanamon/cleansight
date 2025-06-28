from flask import Blueprint, jsonify
from app import db
from models.image import Image
from utils.feature_extraction import extract_features
from utils.rules import load_rules_from_json, classify_image, apply_rules


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
