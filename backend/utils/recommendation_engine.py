import sys
from pathlib import Path
import json
from tqdm import tqdm

from backend.utils.feature_extraction import extract_features
from backend.utils.rules import load_rules_from_json, apply_rules, classify_image

RULES_PATH = "backend/utils/rules.json"

# Dictionnaire de correspondance message rules → recommandation terrain
MESSAGE_TO_RECOMMENDATION = {
    "💡 Poubelle probablement pleine (fichier lourd)": "⚠️ À surveiller : risque de débordement, planifier une collecte rapidement.",
    "💡 Poubelle probablement pleine (fichier léger, couleur sombre)": "⚠️ Image suspecte (sombre), vérifier sur le terrain si la poubelle est vraiment pleine.",
    "💡 Poubelle probablement pleine (faible nombre de contours)": "⚠️ Collecte à planifier : poubelle probablement pleine malgré peu de contours.",
    "💡 Poubelle probablement pleine (beaucoup de contours)": "⚠️ Surcharge possible, intervention recommandée rapidement.",
    "✅ Poubelle probablement vide (fichier léger, couleur claire)": "RAS : pas d’action requise, poubelle probablement vide.",
    "✅ Poubelle probablement vide (contours intermédiaires)": "RAS : poubelle à surveiller, mais pas d’intervention urgente.",
}

def remap_messages_to_recommendations(messages):
    recommendations = []
    for msg in messages:
        reco = MESSAGE_TO_RECOMMENDATION.get(msg)
        if reco:
            recommendations.append(reco)
        else:
            # Si pas de mapping, renvoyer le message original
            recommendations.append(f"(À relire) {msg}")
    return recommendations

def main(folder):
    load_rules_from_json(RULES_PATH)
    folder = Path(folder)
    images = [f for f in folder.iterdir() if f.is_file() and not ("_resized" in f.name or "_compressed" in f.name)]

    results = []
    for img in tqdm(images, desc="Recommandations"):
        feats = extract_features(str(img), resize=False)
        if feats:
            label = classify_image(feats)
            triggered_messages = apply_rules(feats)
            recommendations = remap_messages_to_recommendations(triggered_messages)

            results.append({
                "filename": img.name,
                "label": label,
                "rules_messages": triggered_messages,
                "recommendations": recommendations,
            })

    # Sortie en JSON
    with open("recommendations.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print("✅ Recommandations terrain générées dans recommendations.json")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python recommendation_engine.py <folder>")
    else:
        main(sys.argv[1])
