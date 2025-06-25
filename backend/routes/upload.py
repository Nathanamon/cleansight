import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models.image import Image
from PIL import Image as PILImage

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload():
    from app import db  # ✅ Import local pour éviter les erreurs circulaires

    # Vérifie que le champ 'image' est bien présent dans le formulaire
    if 'image' not in request.files or 'annotation' not in request.form:
        return jsonify({"error": "Image et annotation sont obligatoires"}), 400

    # Récupère le fichier et l’annotation
    image_file = request.files['image']
    annotation = request.form['annotation']

    # Sécurise le nom du fichier (évite les injections de chemin)
    filename = secure_filename(image_file.filename)

    # Enregistre le fichier dans le dossier d'uploads
    upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    image_file.save(upload_path)

    # Ouvre l’image avec PIL pour extraire les dimensions
    pil_image = PILImage.open(upload_path)
    largeur, hauteur = pil_image.size
    taille = os.path.getsize(upload_path)
    couleur_moyenne = str(pil_image.resize((1,1)).getpixel((0,0)))  # simple estimation

    # Crée une instance du modèle Image
    image = Image(
        filename=filename,
        annotation=annotation,
        taille=taille,
        largeur=largeur,
        hauteur=hauteur,
        couleur_moyenne=couleur_moyenne
    )

    # Sauvegarde en base
    db.session.add(image)
    db.session.commit()

    return jsonify({"message": "Image bien enregistrée"}), 201
