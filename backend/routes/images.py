# backend/routes/images.py

from datetime import datetime
from flask import Blueprint, request, jsonify, current_app, send_from_directory


images_bp = Blueprint("images", __name__)

@images_bp.route("/images", methods=["GET"])
def get_images():
    from app import db
    from models.image import Image

    # filtres
    ann = request.args.get("annotation")
    df  = request.args.get("date_from")
    dt  = request.args.get("date_to")

    q = Image.query
    if ann in ("pleine", "vide"):
        q = q.filter_by(annotation=ann)
    if df:
        q = q.filter(Image.date_upload >= datetime.fromisoformat(df))
    if dt:
        q = q.filter(Image.date_upload <= datetime.fromisoformat(dt))

    images = q.order_by(Image.id.asc()).all()
    data = []
    for img in images:
        data.append({
            "id":               img.id,
            "filename":         img.filename,
            "date_upload":      img.date_upload.isoformat(),
            "annotation":       img.annotation,
            "annotation_auto":  img.annotation_auto,
            "taille":           img.taille,
            "largeur":          img.largeur,
            "hauteur":          img.hauteur,
            "contraste":        img.contraste,
            "couleur_moyenne":  img.couleur_moyenne,
            "metadata":    img.metadata_json
        })
    return jsonify(data), 200


@images_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_image(filename):
    """Return an uploaded image file."""
    folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(folder, filename)