from dotenv import load_dotenv
import os

# Charger les variables d'environnement depuis .env
load_dotenv()

# Répertoire racine du projet
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configuration de l'application Flask"""
    # Clés secrètes
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-in-prod")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "change-this-in-prod")
    

    # Base de données
    # IMPORTANT: l'env doit définir DATABASE_URL, pas DB_URL
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("DATABASE_URL")
        or "postgresql://postgres1:dww3PXKZHq6HSBYukXOEmSRWjdWceVzy@dpg-d1mjq50dl3ps73dk987g-a/poubelle_db_u8pi"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Dossier d'uploads
    UPLOAD_FOLDER = os.path.join(basedir, "uploads")

    # Sessions
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # À mettre True en production (HTTPS)

    # Mail (SendGrid)
    MAIL_SERVER = "smtp.sendgrid.net"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "apikey")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_DEFAULT_SENDER = ("CleanSight", "noreply@cleansight.com")

    # JWT (cookies)
    JWT_TOKEN_LOCATION = ["cookies", "headers"]
    JWT_COOKIE_SECURE = False  # True en production
    # En développement la valeur "None" requiert l'option Secure et le cookie
    # est ignoré par le navigateur. On utilise donc "Lax" pour que les cookies
    # d'authentification soient bien envoyés sur http://localhost.
    JWT_COOKIE_SAMESITE = "Lax"
    JWT_ACCESS_COOKIE_PATH = "/"
    JWT_REFRESH_COOKIE_PATH = "/auth/refresh"
    JWT_COOKIE_CSRF_PROTECT = True  # Protection CSRF pour les cookies JWT
    JWT_CSRF_IN_COOKIES = False
    




    # Validation des codes agents
    # On accepte uniquement les codes au format AGP- suivis de 4 chiffres
    AGENT_CODE_PATTERN = r"^AGP-\d{4}$"
    # Optionnel : liste personnalisée via variable d'env (séparée par des virgules)
    VALID_AGENT_CODES = [
        code.strip()
        for code in os.environ.get("VALID_AGENT_CODES", "").split(",")
        if code.strip()
    ]