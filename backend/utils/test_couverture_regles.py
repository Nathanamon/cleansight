import os
import json
from pathlib import Path
from backend.utils.rules import load_rules_from_json, apply_rules
import pandas as pd
from backend.utils.feature_extraction import extract_features
from collections import defaultdict

# Chemins
DIR_CLEAN = "Data/train/with_label/clean"
DIR_DIRTY = "Data/train/with_label/dirty"
RULES_JSON = "backend/utils/rules.json"

def collect_features(img_dir):
    data = []
    for fname in os.listdir(img_dir):
        if not fname.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.webp', '.tiff')):
            continue
        path = str(Path(img_dir) / fname)
        feats = extract_features(path, resize=False)
        if feats:
            feats['filename'] = fname
            data.append(feats)
    return data

def main():
    # Charger les règles
    load_rules_from_json(RULES_JSON)
    # Collecter features
    data_clean = collect_features(DIR_CLEAN)
    data_dirty = collect_features(DIR_DIRTY)
    print(f"{len(data_clean)} clean, {len(data_dirty)} dirty images analysées.")

    # Comptage par règle
    rule_hits = defaultdict(lambda: {"clean": 0, "dirty": 0})

    for feats in data_clean:
        msgs = apply_rules(feats)
        for msg in msgs:
            rule_hits[msg]["clean"] += 1

    for feats in data_dirty:
        msgs = apply_rules(feats)
        for msg in msgs:
            rule_hits[msg]["dirty"] += 1

    # Comptage des non-classés
    n_unclassified_clean = sum(1 for f in data_clean if not apply_rules(f))
    n_unclassified_dirty = sum(1 for f in data_dirty if not apply_rules(f))

    # Affichage résumé
    print("\n=== Couverture des règles ===")
    print(f"{'Règle':55} | Clean | Dirty")
    print("-"*70)
    for rule, counts in rule_hits.items():
        print(f"{rule:55} | {counts['clean']:5d} | {counts['dirty']:5d}")
    print("-"*70)
    print(f"Non classés (clean): {n_unclassified_clean} / {len(data_clean)}")
    print(f"Non classés (dirty): {n_unclassified_dirty} / {len(data_dirty)}")

if __name__ == "__main__":
    main()
