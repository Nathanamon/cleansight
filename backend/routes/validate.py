# backend/routes/validate.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from app import db
from models.image import Image
from utils.feature_extraction import extract_features
from utils.metadata_generator import generate_metadata
# (PIL n'est plus utilisé directement ici)

validate_bp = Blueprint("validate", __name__)

@validate_bp.route("/validate", methods=["POST"])
def validate():
    if 'image' not in request.files or 'label' not in request.form:
        return jsonify({"error": "Image et label sont obligatoires"}), 400

    img_file = request.files['image']
    label    = request.form['label']
    annotation_auto = request.form.get('prediction')  # <--- tu peux le passer depuis le front si besoin
    fname    = secure_filename(img_file.filename)

    folder = current_app.config["UPLOAD_FOLDER"]
    fullpath = os.path.join(folder, fname)
    img_file.save(fullpath)

    features = extract_features(fullpath)
    metadata = generate_metadata()

    if not features:
        return jsonify({"error": "Impossible d'extraire les caractéristiques"}), 400
    
    annotation_auto = request.form.get("annotation_auto", None)

    record = Image(
        filename    = fname,
        date_upload = datetime.utcnow(),
        annotation  = label,
        largeur     = features["width"],            # anciennement 'largeur'
        hauteur     = features["height"],           # anciennement 'hauteur'
        taille      = features["file_size"],        # anciennement 'taille'
        contraste   = features["rms_contrast"],     # anciennement 'contraste'
        annotation_auto = annotation_auto,
        couleur_moyenne = f"{features['mean_r']:.1f},{features['mean_g']:.1f},{features['mean_b']:.1f}",  # string RGB
        metadata_json = metadata               # JSON des métadonnées
        # tu peux stocker d’autres features si tu veux...
    )
    db.session.add(record)
    db.session.commit()


    return jsonify({
        "message": "Image enregistrée avec succès",
        "metadata": metadata,
        }), 201
