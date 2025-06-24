"""
Moteur de recommandations CleanSight
====================================

Ce module :
    - Extrait les features d'une image ou d'un dossier d'images
    - Applique les règles métiers depuis rules.json
    - Génère un label ("pleine"/"vide") et des messages d'action
    - Calcule éventuellement un score d'hygiène ("cleanscore")

Dépendances : feature_extraction.py, rules.py, rules.json
"""
import os
from typing import Dict, List, Any, Optional

from backend.utils.feature_extraction import extract_features
from backend.utils.rules import load_rules_from_json, apply_rules, classify_image

RULES_PATH = "backend/utils/rules.json"

def recommend_for_image(image_path: str) -> Dict[str, Any]:
    """
    Traite une image : extraction features, classification, recommandations.
    """
    # 1. Extraction des features
    feats = extract_features(image_path, resize=True)
    if feats is None:
        return {
            "image_path": image_path,
            "error": "Extraction des features impossible"
        }

    # 2. Application des règles
    label = classify_image(feats)
    recommendations = apply_rules(feats)
    # 3. Score simple : plus il y a de règles “critiques” déclenchées, plus le cleanscore baisse
    cleanscore = 100
    if any("pleine" in r for r in recommendations):
        cleanscore -= 50
    if any("sombre" in r for r in recommendations):
        cleanscore -= 25
    if any("trop petite" in r for r in recommendations):
        cleanscore -= 10

    return {
        "image_path": image_path,
        "features": feats,
        "label": label,
        "recommendations": recommendations,
        "cleanscore": cleanscore
    }

def recommend_batch(images: List[str]) -> List[Dict[str, Any]]:
    """
    Traite une liste d'images.
    """
    results = []
    for img_path in images:
        results.append(recommend_for_image(img_path))
    return results

if __name__ == "__main__":
    import argparse
    from pathlib import Path
    from tqdm import tqdm

    parser = argparse.ArgumentParser(description="CleanSight Recommendation Engine")
    parser.add_argument("path", help="Image ou dossier à traiter")
    parser.add_argument("--rules", default=RULES_PATH, help="Chemin rules.json")
    args = parser.parse_args()

    load_rules_from_json(args.rules)

    path = Path(args.path)
    images = []
    if path.is_dir():
        for ext in ["jpg", "jpeg", "png"]:
            images += list(path.glob(f"**/*.{ext}"))
        print(f"{len(images)} images trouvées.")
    else:
        images = [path]

    results = []
    for img_path in tqdm(images, desc="Recommandations"):
        result = recommend_for_image(str(img_path))
        results.append(result)
        print(f"{os.path.basename(str(img_path))}: {result['label']} — {', '.join(result['recommendations'])}")

    # Optionnel: sauvegarder en CSV/JSON
    import json
    with open("recommendations.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("✅ Recommandations terminées et sauvegardées dans recommendations.json")
