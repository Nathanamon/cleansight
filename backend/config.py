# backend/config.py

import os

# calcul du répertoire racine du projet
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # URL de connexion à PostgreSQL — adaptez user/password/host/dbname
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres:Mylie2025@localhost/poubelle_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # dossier où on sauvegarde les uploads
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")
