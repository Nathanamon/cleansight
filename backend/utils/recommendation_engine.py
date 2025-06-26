import os
import json
from pathlib import Path
from tqdm import tqdm
from backend.utils.feature_extraction import extract_features
from backend.utils.rules import load_rules_from_json, classify_image, apply_rules

# Mapping messages → recommandations actionnables
MESSAGE_TO_ACTION = {
    "✅ Poubelle probablement vide":
        "ℹ️ Surveillance minimale requise, collecte non prioritaire.",
    "💡 Poubelle pleine (petite hauteur, peu de contours, basse luminosité bleue)":
        "⚠️ Collecte à planifier rapidement (poubelle probablement pleine, basse hauteur, faible luminosité).",
    "✅ Poubelle probablement vide (haute résolution, beaucoup de contours)":
        "🟢 Image de bonne qualité, poubelle probablement vide : surveillance simple.",
    "💡 Poubelle pleine (hauteur moyenne, fichier lourd, faible rouge)":
        "⚠️ Collecte à prévoir : fichier lourd et faible valeur de rouge détecté.",
    "💡 Poubelle pleine (grande image, rouge faible)":
        "⚠️ Contrôle manuel conseillé (grande poubelle détectée, rouge faible)."
}

def is_image_file(filename):
    ext = filename.lower().split('.')[-1]
    return ext in {"jpg", "jpeg", "png", "bmp", "webp", "tiff"}

def main(images_dir, rules_json="rules.json"):
    # Charge les règles
    load_rules_from_json(rules_json)

    images = [
        f for f in os.listdir(images_dir)
        if is_image_file(f) and "_resized" not in f and "_compressed" not in f
    ]

    if not images:
        print("Aucune image trouvée dans", images_dir)
        return

    output = []
    print(f"{len(images)} images trouvées.\n")

    for img_name in tqdm(images, desc="Recommandations"):
        img_path = str(Path(images_dir) / img_name)
        feats = extract_features(img_path)
        if feats is None:
            print(f"❌ Extraction impossible sur {img_name}")
            continue

        # Appliquer règles + recommandations
        triggered_msgs = apply_rules(feats)
        reco = [MESSAGE_TO_ACTION.get(m, m) for m in triggered_msgs]
        label = classify_image(feats)

        output.append({
            "filename": img_name,
            "label": label,
            "rules_messages": triggered_msgs,
            "recommendations": reco
        })

    with open("recommendations.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print("\n✅ Recommandations terrain générées dans recommendations.json")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python recommendation_engine.py <repertoire_images> [rules.json]")
    else:
        images_dir = sys.argv[1]
        rules_path = sys.argv[2] if len(sys.argv) > 2 else "rules.json"
        main(images_dir, rules_path)

