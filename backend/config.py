# backend/config.py

import os

# calcul du répertoire racine du projet
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration de l'application Flask."""
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres:informatitien@localhost/poubelle_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # dossier où on sauvegarde les uploads
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")
