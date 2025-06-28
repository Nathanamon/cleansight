import os
import glob
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from fpdf import FPDF
from backend.utils.feature_extraction import extract_features
from backend.utils.rules import load_rules_from_json, classify_image, apply_rules

DATA_ROOT = "Data/train/"
RULES_PATH = "backend/utils/rules.json"

image_paths = []
for main_dir in ["with_label", "no_label"]:
    base_path = os.path.join(DATA_ROOT, main_dir)
    if not os.path.exists(base_path):
        continue
    subfolders = ["dirty", "clean"] if main_dir == "with_label" else [""]
    for label in subfolders:
        search_path = os.path.join(base_path, label) if label else base_path
        for ext in ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"):
            image_paths.extend(glob.glob(os.path.join(search_path, ext)))

print(f"🚀 {len(image_paths)} images trouvées. Début pipeline...")

load_rules_from_json(RULES_PATH)

results = []
errors = []
for img_path in tqdm(image_paths, desc="Pipeline extraction + classification"):
    try:
        features = extract_features(img_path, resize=False)
        if features:
            label = classify_image(features)
            recommendations = apply_rules(features)
            row = features.copy()
            row["filename"] = os.path.relpath(img_path, DATA_ROOT)
            row["auto_label"] = label
            row["recommendations"] = "; ".join(recommendations)
            results.append(row)
        else:
            errors.append(img_path)
    except Exception as e:
        errors.append(f"{img_path} | {str(e)}")

df = pd.DataFrame(results)
df.to_csv("pipeline_results.csv", index=False, encoding="utf-8")
print(f"✅ Pipeline terminé : {len(df)} images traitées, résultats dans pipeline_results.csv.")

# --------------- Génération du log d’erreur ---------------
if errors:
    with open("errors.log", "w", encoding="utf-8") as logf:
        for err in errors:
            logf.write(f"{err}\n")
    print(f"⚠️ {len(errors)} images en échec, détails dans errors.log")
else:
    print("✅ Aucun échec d’extraction !")

# --------------- Génération du rapport summary.txt ---------------
now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
total = len(image_paths)
ok = len(df)
failed = len(errors)
pleine = sum(df["auto_label"] == "pleine")
vide = sum(df["auto_label"] == "vide")
autres = ok - pleine - vide

summary = f"""
CleanSight - Rapport d'extraction automatique
Généré le : {now}

Images totales traitées : {total}
    - Succès        : {ok}
    - Échecs        : {failed}
    - Label 'pleine': {pleine}
    - Label 'vide'  : {vide}
    - Autres/None   : {autres}

CSV complet : pipeline_results.csv
Log erreurs : errors.log

Premiers labels (échantillon) :
{df[['filename', 'auto_label', 'recommendations']].head(10).to_string(index=False)}
"""

with open("summary.txt", "w", encoding="utf-8") as sf:
    sf.write(summary.strip())

print("📄 Rapport 'summary.txt' généré.")