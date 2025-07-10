from main import create_app, db
from models.image import Image

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Table image créée avec succès")
