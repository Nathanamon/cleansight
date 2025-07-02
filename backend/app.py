import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from utils.rules import load_rules_from_json

# Une unique instance de SQLAlchemy
db = SQLAlchemy()

def create_app():
    # 1. Création de l’app Flask
    app = Flask(__name__)
    app.config.from_object(Config)

    # 2. Création du dossier d'uploads si nécessaire
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # 3. CORS (toutes origines autorisées)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # 4. Init de SQLAlchemy
    db.init_app(app)

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

    return app

if __name__ == "__main__":
    # Lance l’app en mode debug
    app = create_app()
    app.run(debug=True)
