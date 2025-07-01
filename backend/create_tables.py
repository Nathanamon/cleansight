# scripts/create_tables.py

from app import create_app, db
# on importe vos modèles pour qu'ils soient pris en compte par SQLAlchemy
import models.image  
import models.user   

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès.")
