import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from utils.rules import load_rules_from_json
from flask_mail import Mail
from flask_jwt_extended import JWTManager

# Une unique instance de SQLAlchemy
db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()

def create_app():
    # 1. Création de l’app Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. Création du dossier d'uploads si nécessaire
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # 3. CORS (toutes origines autorisées)
    CORS(
        app,
        resources={r"/*": {"origins": "http://localhost:5173"}},  # votre front Vite
        supports_credentials=True,
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    # 4. Init de SQLAlchemy
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)

    # 5. Chargement des règles métier dès le démarrage
    rules_path = os.path.join(app.root_path, "utils", "rules.json")
    load_rules_from_json(rules_path)

    # 6. Enregistrement de tous les blueprints

    # → Upload (POST /upload)
    from routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    # → Images (GET /images)
    from routes.images import images_bp
    app.register_blueprint(images_bp)

    # → Predict (POST /predict)
    from routes.predict import predict_bp
    app.register_blueprint(predict_bp)

    # → Validate (POST /validate)
    from routes.validate import validate_bp
    app.register_blueprint(validate_bp)
    
    from routes.auth     import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    return app

if __name__ == "__main__":
    # Lance l’app en mode debug
    app = create_app()
    app.run(debug=True)
