import json
from flask import Blueprint, jsonify

recommendation_bp = Blueprint("recommendation", __name__, url_prefix="/dashboard")

@recommendation_bp.route("/recommendations", methods=["GET"])
def get_recommendations():
    """Serve les recommandations IA à partir du fichier JSON généré."""
    try:
        with open("recommendations.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data), 200
    except FileNotFoundError:
        return jsonify({"error": "Aucune recommandation disponible."}), 404
    except json.JSONDecodeError:
        return jsonify({"error": "Erreur de lecture du fichier de recommandations."}), 500

@recommendation_bp.route("/generate_recommendations", methods=["POST"])
def generate_recommendations():
    try:
        import subprocess
        subprocess.run(["python", "utils/generate_recommendations.py"], check=True)
        return jsonify({"message": "Recommandations générées avec succès"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
