from datetime import datetime, timedelta, timezone
import os
from sqlalchemy import create_engine, text
import json

# Configuration de la base de données
DATABASE_URL = "postgresql://postgres1:dww3PXKZHq6HSBYukXOEmSRWjdWceVzy@dpg-d1mjq50dl3ps73dk987g-a.frankfurt-postgres.render.com/poubelle_db_u8pi"

# Connexion à PostgreSQL
engine = create_engine(DATABASE_URL)

# Définir la période d’analyse (ex : 7 derniers jours)
now = datetime.now(timezone.utc)
start_date = now - timedelta(days=7)

# Requête : images avec annotation et métadonnées
query = text("""
SELECT id, filename, annotation, annotation_auto, date_upload, metadata_json
FROM image
WHERE date_upload >= :start_date
""")

with engine.connect() as conn:
    result = conn.execute(query, {"start_date": start_date}).fetchall()

# Analyse des données
zone_stats = {}
upload_count = {}
maintenance_count = 0

for row in result:
    metadata = row.metadata_json or {}
    annotation = row.annotation_auto or row.annotation
    date_str = row.date_upload.date().isoformat()

    location = metadata.get("location", {})
    address = location.get("address", "Inconnue")
    zipcode = address.split(",")[-2].strip().split(" ")[0] if "," in address else "Inconnue"

    weather = metadata.get("weather", {})
    if annotation == "pleine":
        zone_stats.setdefault(zipcode, {"pleine": 0, "total": 0})
        zone_stats[zipcode]["pleine"] += 1
    zone_stats.setdefault(zipcode, {"pleine": 0, "total": 0})
    zone_stats[zipcode]["total"] += 1

    # Comptage des uploads
    upload_count[date_str] = upload_count.get(date_str, 0) + 1

    # Maintenance
    if annotation == "maintenance":
        maintenance_count += 1

# Générer les recommandations
recs = []

for code_postal, stats in zone_stats.items():
    taux = stats["pleine"] / stats["total"] if stats["total"] else 0
    if taux > 0.4:
        recs.append({
            "title": f"Augmenter les collectes dans le {code_postal}",
            "description": f"Le taux de remplissage est élevé ({taux*100:.0f}%) dans cette zone.",
            "icon": "fas fa-map-marker-alt",
            "severity": "high"
        })

# Pic d’activité
if upload_count:
    max_day = max(upload_count, key=upload_count.get)
    if upload_count[max_day] > 10:
        recs.append({
            "title": f"Surveillance renforcée le {max_day}",
            "description": f"{upload_count[max_day]} images ont été uploadées ce jour-là.",
            "icon": "fas fa-chart-line",
            "severity": "medium"
        })


# Trop de bacs en maintenance
if maintenance_count >= 5:
    recs.append({
        "title": "Planifier des entretiens techniques",
        "description": f"{maintenance_count} poubelles en maintenance détectées.",
        "icon": "fas fa-tools",
        "severity": "medium"
    })

# Écriture dans un fichier JSON
output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "static"))
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "recommendations.json")

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(recs, f, ensure_ascii=False, indent=2)

print("✅ Recommandations sauvegardées dans recommendations.json")
