# backend/routes/images.py

from datetime import datetime
import os
from flask import Blueprint, request, jsonify, current_app, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity

images_bp = Blueprint("images", __name__)

@images_bp.route("/images", methods=["GET"])
def get_images():
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
            "metadata":         img.metadata_json,
        })
    return jsonify(data), 200


@images_bp.route("/images/<int:image_id>", methods=["DELETE"])
@jwt_required()
def delete_image(image_id):
    """Delete an uploaded image and its record."""
    from cleansight.backend.main import db
    from models.image import Image

    user_id = get_jwt_identity()
    img = Image.query.filter_by(id=image_id, user_id=user_id).first()
    if img is None:
        return jsonify({"error": "Image not found"}), 404

    folder = current_app.config["UPLOAD_FOLDER"]
    path = os.path.join(folder, img.filename)
    if os.path.exists(path):
        os.remove(path)

    db.session.delete(img)
    db.session.commit()

    return jsonify({"message": "Image supprimée"}), 200

@images_bp.route("/images/<int:image_id>", methods=["PATCH"])
def update_image(image_id):
    from cleansight.backend.main import db
    from models.image import Image

    data = request.get_json() or {}
    new_ann = data.get("annotation")
    if new_ann not in ("pleine", "vide","vidée", "maintenance", "débordante"):
        return jsonify({"error": "Annotation invalide"}), 400

    img = Image.query.filter_by(id=image_id).first()
    if img is None:
        return jsonify({"error": "Image not found"}), 404

    img.annotation = new_ann
    db.session.commit()

    return jsonify({"message": "Image mise à jour"}), 200



@images_bp.route('/uploads/<path:filename>', methods=['GET'])
def serve_image(filename):
    """Return an uploaded image file."""
    folder = current_app.config['UPLOAD_FOLDER']
    return send_from_directory(folder, filename)