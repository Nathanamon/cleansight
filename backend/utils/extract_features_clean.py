import os
import csv
from tqdm import tqdm
from backend.utils.feature_extraction import extract_features

CLEAN_DIR = "Data/train/with_label/dirty"  # Dossier avec images à nettoyer
OUT_CSV = "features_dirty.csv"

def is_image_file(filename):
    ext = filename.lower().split('.')[-1]
    return ext in {"jpg", "jpeg", "png", "bmp", "webp", "tiff"}

def main():
    # On ignore les images resized/compressed pour éviter les doublons et fausses stats
    files = [
        f for f in os.listdir(CLEAN_DIR)
        if is_image_file(f) and "_resized" not in f and "_compressed" not in f
    ]
    print(f"{len(files)} images trouvées dans {CLEAN_DIR}")

    all_features = []
    for fname in tqdm(files, desc="Extraction features"):
        path = os.path.join(CLEAN_DIR, fname)
        features = extract_features(path, resize=False)
        if features:
            features["filename"] = fname
            all_features.append(features)
        else:
            print(f"❌ Problème sur {fname}")

    if not all_features:
        print("Aucune feature extraite, vérifie le dossier et les dépendances.")
        return

    keys = ["filename"] + [k for k in all_features[0] if k != "filename" and k != "histogram"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        for feat in all_features:
            row = {k: feat[k] for k in keys}
            writer.writerow(row)
    print(f"✅ Fichier features_dirty.csv généré ({len(all_features)} images).")

if __name__ == "__main__":
    main()

