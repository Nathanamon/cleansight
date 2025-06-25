from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    from routes.upload import upload_bp  # ✅ METS-LA ICI
    app.register_blueprint(upload_bp)

    from models.image import Image  # ok ici aussi
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
