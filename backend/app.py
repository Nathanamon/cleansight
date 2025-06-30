import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from utils.rules import load_rules_from_json

# créez une unique instance de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # création du dossier d'upload si besoin
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    
    # CORS sur tout
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)

    # chargement des règles en mémoire dès le démarrage
    rules_path = os.path.join(app.root_path, "utils", "rules.json")
    load_rules_from_json(rules_path)

    # blueprints
    #from routes.upload import upload_bp
    # app.register_blueprint(upload_bp) # désactivé : plus d'endpoint /upload
    from routes.images import images_bp
    app.register_blueprint(images_bp)
    from routes.predict import predict_bp
    app.register_blueprint(predict_bp)
    from routes.validate import validate_bp
    app.register_blueprint(validate_bp)

    return app