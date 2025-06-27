# backend/routes/upload.py

import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db                # instance SQLAlchemy unique
from models.image import Image    # votre modèle

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload():
    # vérification
    if 'image' not in request.files or 'annotation' not in request.form:
        return jsonify({"error": "Image et annotation sont obligatoires"}), 400

    image_file = request.files['image']
    annotation = request.form['annotation']
    filename = secure_filename(image_file.filename)

    # chemin complet
    upload_folder = current_app.config['UPLOAD_FOLDER']
    path = os.path.join(upload_folder, filename)
    image_file.save(path)

    # lecture pour extraire taille et dimensions
    from PIL import Image as PILImage
    pil = PILImage.open(path)
    largeur, hauteur = pil.size
    taille = os.path.getsize(path)

    # création de l’objet SQLAlchemy
    img = Image(
        filename=filename,
        date_upload=datetime.utcnow(),
        annotation=annotation,
        largeur=largeur,
        hauteur=hauteur,
        taille=taille
    )
    db.session.add(img)
    db.session.commit()

    return jsonify({"message": "Image enregistrée avec succès"}), 201
