import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail

from config import Config
from utils.rules import load_rules_from_json

# — Extensions globales —————————————————————————————————————————————
db   = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(Config)

    # Crée le dossier d’uploads si nécessaire
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Init des extensions
    db.init_app(app)
    mail.init_app(app)
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:5173"}},  # votre front Vite
        supports_credentials=True,
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # Chargement des règles une fois pour toutes
    rules_path = os.path.join(app.root_path, "utils", "rules.json")
    load_rules_from_json(rules_path)

    # — Blueprints ————————————————————————————————————————————————
    from routes.images   import images_bp
    from routes.predict  import predict_bp
    from routes.validate import validate_bp
    from routes.auth     import auth_bp

    app.register_blueprint(images_bp)                  # /images
    app.register_blueprint(predict_bp)                 # /predict
    app.register_blueprint(validate_bp)                # /validate
    app.register_blueprint(auth_bp, url_prefix="/auth")# /auth/signup, /auth/login, etc.

    return app