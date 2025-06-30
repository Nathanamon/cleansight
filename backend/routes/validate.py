# backend/routes/validate.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from models.image import Image
from PIL import Image as PILImage

validate_bp = Blueprint("validate", __name__)

@validate_bp.route("/validate", methods=["POST"])
def validate():
    # même signature que votre ancien /upload
    if 'image' not in request.files or 'label' not in request.form:
        return jsonify({"error": "Image et label sont obligatoires"}), 400

    img_file = request.files['image']
    label    = request.form['label']
    fname    = secure_filename(img_file.filename)

    folder = current_app.config["UPLOAD_FOLDER"]
    fullpath = os.path.join(folder, fname)
    img_file.save(fullpath)

    # extraire dims & taille
    pil = PILImage.open(fullpath)
    largeur, hauteur = pil.size
    taille = os.path.getsize(fullpath)

    # enregistrer en BDD
    record = Image(
        filename    = fname,
        date_upload = datetime.utcnow(),
        annotation  = label,
        largeur     = largeur,
        hauteur     = hauteur,
        taille      = taille
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({"message": "Image enregistrée avec succès"}), 201