# backend/config.py
from dotenv import load_dotenv
load_dotenv()   # va charger automatiquement .env


import os

# calcul du répertoire racine du projet
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-en-prod")
    """Configuration de l'application Flask."""
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres:informatitien@localhost/poubelle_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # dossier où on sauvegarde les uploads
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")
    
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
 
    MAIL_SERVER   = "smtp.sendgrid.net"
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = "apikey"                      # obligatoirement “apikey”
    MAIL_PASSWORD = os.environ["SENDGRID_API_KEY"]
    MAIL_DEFAULT_SENDER = ("CleanSight", "noreplycleansigth@gmail.com")
    SECRET_KEY = os.environ["SECRET_KEY"]
