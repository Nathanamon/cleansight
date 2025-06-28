# backend/routes/predict.py
import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from utils.feature_extraction import extract_features
from utils.rules import load_rules_from_json, classify_image, apply_rules

predict_bp = Blueprint("predict", __name__)

@predict_bp.route("/predict", methods=["POST"])
def predict():
    if 'image' not in request.files:
        return jsonify({"error": "Image is required"}), 400

    img = request.files['image']
    fname = secure_filename(img.filename)
    tmp = os.path.join(current_app.config["UPLOAD_FOLDER"], f"tmp_{fname}")
    img.save(tmp)

    feats = extract_features(tmp, resize=False)
    os.remove(tmp)

    if feats is None:
        return jsonify({"label": None}), 200

    label = classify_image(feats)  # renvoie "pleine", "vide" ou None
    return jsonify({"label": label}), 200

