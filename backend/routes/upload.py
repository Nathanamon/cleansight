# backend/routes/upload.py
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from datetime import datetime
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from main import db
from models.image import Image
from feature_extraction import extract_features
from classification import classify_image
from utils.metadata_generator import generate_metadata


upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
@jwt_required()
def upload():
    if 'image' not in request.files or 'annotation' not in request.form:
        return jsonify({"error": "Image et annotation sont obligatoires"}), 400

    file       = request.files['image']
    manual_ann = request.form['annotation']
    filename   = secure_filename(file.filename)
    folder     = current_app.config['UPLOAD_FOLDER']
    os.makedirs(folder, exist_ok=True)
    base, ext = os.path.splitext(filename)
    unique_name = filename
    counter = 1
    while os.path.exists(os.path.join(folder, unique_name)):
        unique_name = f"{base}_{counter}{ext}"
        counter += 1

    path = os.path.join(folder, unique_name)
    file.save(path)

    features = extract_features(path)
    auto_ann = classify_image(features)
    metadata = generate_metadata()
    user_id = get_jwt_identity()


    img = Image(
        filename=unique_name,
        user_id=user_id,
        date_upload=datetime.utcnow(),
        annotation=manual_ann,
        annotation_auto=auto_ann,
        taille=features["taille"],
        largeur=features["largeur"],
        hauteur=features["hauteur"],
        contraste=features["contraste"],
        couleur_moyenne=features["couleur_moyenne"],
        metadata_json=metadata
    )
    db.session.add(img)
    db.session.commit()

    return jsonify({
        "message": "Image enregistrée avec succès",
        "annotation_auto": auto_ann,
        "metadata": metadata,
        "log": f"Image {unique_name} enregistrée avec annotation: {manual_ann}, auto-annotation: {auto_ann}, metadata: {metadata}"
    }), 201
