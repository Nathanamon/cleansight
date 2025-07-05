# backend/routes/validate.py
import os
from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from models.image import Image
from utils.feature_extraction import extract_features
from utils.metadata_generator import generate_metadata
# (PIL n'est plus utilisé directement ici)

validate_bp = Blueprint("validate", __name__)

@validate_bp.route("/validate", methods=["POST"])
@jwt_required()
def validate():
    if 'image' not in request.files or 'label' not in request.form:
        return jsonify({"error": "Image et label sont obligatoires"}), 400

    img_file = request.files['image']
    label    = request.form['label']
    user_id  = get_jwt_identity()
    if user_id is None:
        return jsonify({"error": "Utilisateur non authentifié"}), 401
    annotation_auto = request.form.get('annotation_auto') or request.form.get('prediction')
    fname    = secure_filename(img_file.filename)

    folder = current_app.config["UPLOAD_FOLDER"]
    os.makedirs(folder, exist_ok=True)  # ensure folder exists
    fullpath = os.path.join(folder, fname)
    img_file.save(fullpath)

    features = extract_features(fullpath)
    if not features:
        # Remove the saved file if feature extraction fails
        if os.path.exists(fullpath):
            os.remove(fullpath)
        return jsonify({"error": "Impossible d'extraire les caractéristiques"}), 400

    metadata = generate_metadata()

    try:
        record = Image(
            user_id     = user_id,
            filename    = fname,
            date_upload = datetime.utcnow(),
            annotation  = label,
            largeur     = features.get("width"),
            hauteur     = features.get("height"),
            taille      = features.get("file_size"),
            contraste   = features.get("rms_contrast"),
            annotation_auto = annotation_auto,
            couleur_moyenne = f"{features.get('mean_r',0):.1f},{features.get('mean_g',0):.1f},{features.get('mean_b',0):.1f}",
            metadata_json = metadata
        )
        db.session.add(record)
        db.session.commit()
    except Exception as e:
        # Clean up file if DB commit fails
        if os.path.exists(fullpath):
            os.remove(fullpath)
        db.session.rollback()
        return jsonify({"error": f"Erreur lors de l'enregistrement: {str(e)}"}), 500

    return jsonify({
        "message": "Image enregistrée avec succès",
        "id": record.id,
        "metadata": metadata,
    }), 201
