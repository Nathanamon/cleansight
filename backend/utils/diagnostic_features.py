import os
from backend.utils.feature_extraction import extract_features
from backend.utils.rules import load_rules_from_json, classify_image, apply_rules

# Adapter le chemin selon ton arborescence
FOLDER = "Data/train/with_label/clean"
RULES = "backend/utils/rules.json"  

def is_image_file(filename):
    ext = filename.lower().split('.')[-1]
    return ext in {"jpg", "jpeg", "png", "bmp", "webp", "tiff"}

def main():
    load_rules_from_json(RULES)
    files = [f for f in os.listdir(FOLDER) if is_image_file(f)]
    for fname in files:
        path = os.path.join(FOLDER, fname)
        feats = extract_features(path, resize=False)
        if feats is None:
            print(f"❌ {fname}: Extraction impossible")
            continue
        label = classify_image(feats)
        messages = apply_rules(feats)
        # Affiche features clés + label + règles déclenchées
        print(f"{fname}:")
        print(f"  Features: height={feats.get('height')}, contour_count={feats.get('contour_count')}, mean_b={feats.get('mean_b')}, mean_g={feats.get('mean_g')}, mean_r={feats.get('mean_r')}, file_size={feats.get('file_size')}")
        print(f"  Prédit: {label or 'non déterminé'} — Règle(s): {messages}")
        print("-" * 60)

if __name__ == "__main__":
    main()