# backend/app.py

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# créez une unique instance de SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # création du dossier d'upload si besoin
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)

    # enregistrement des routes
    from routes.upload import upload_bp
    app.register_blueprint(upload_bp)

    from routes.images import images_bp
    app.register_blueprint(images_bp)

    return app
