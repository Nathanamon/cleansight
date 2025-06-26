import os
import json
from pathlib import Path
from tqdm import tqdm
from backend.utils.feature_extraction import extract_features
from backend.utils.rules import load_rules_from_json, classify_image, apply_rules

def is_image_file(filename):
    ext = filename.lower().split('.')[-1]
    return ext in {"jpg", "jpeg", "png", "bmp", "webp", "tiff"}

def main(images_dir, rules_json="rules.json"):
    # Charge les règles
    load_rules_from_json(rules_json)

    # Liste des images à traiter
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
        feats = extract_features(img_path, resize=False)
        if feats is None:
            print(f"❌ Extraction impossible sur {img_name}")
            continue

        # Appliquer règles
        triggered_msgs = apply_rules(feats)

        # Générer recommandations orientées collectivités
        reco = []
        for m in triggered_msgs:
            if m.startswith("✅ Poubelle vide"):
                reco.append(
                    "ℹ️ Surveillance minimale requise, collecte non prioritaire."
                )
            elif m.startswith("💡 Poubelle pleine"):
                reco.append(
                    "⚠️ Collecte prioritaire à planifier immédiatement (poubelle probablement pleine)."
                )
            else:
                # Cas générique
                reco.append(f"⚠️ Action requise : {m}")

        label = classify_image(feats)

        output.append({
            "filename": img_name,
            "label": label,
            "rules_messages": triggered_msgs,
            "recommendations": reco
        })

        # Affichage console
        msgs = ", ".join(triggered_msgs) if triggered_msgs else "Aucune recommandation"
        print(f"{img_name}: {label or 'non déterminé'} — {msgs}")

    # Sauvegarde des recommandations
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
