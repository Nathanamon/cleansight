import pandas as pd
from backend.utils.rules import classify_image, load_rules_from_json

# Charger les features
df_clean = pd.read_csv('features_clean.csv')
df_dirty = pd.read_csv('features_dirty.csv')
df_clean.set_index('filename', inplace=True)
df_dirty.set_index('filename', inplace=True)

# Charger les règles
load_rules_from_json("backend/utils/rules.json")

# Pour stocker les images mal classées
clean_misclassified = []
dirty_misclassified = []

# CLEAN : doivent être "vide"
for filename, row in df_clean.iterrows():
    pred = classify_image(row.to_dict())
    if pred != "vide":
        clean_misclassified.append((filename, pred))

# DIRTY : doivent être "pleine"
for filename, row in df_dirty.iterrows():
    pred = classify_image(row.to_dict())
    if pred != "pleine":
        dirty_misclassified.append((filename, pred))

def print_features(image_name, features_df):
    print(f"--- {image_name} ---")
    print(features_df.loc[image_name])
    print("---------------------\n")

print("=== CLEAN mal classés (prédits non-vide) ===")
for img, pred in clean_misclassified:
    print(f"{img}: prédit {pred}")
    print_features(img, df_clean)

print("=== DIRTY mal classés (prédits non-pleine) ===")
for img, pred in dirty_misclassified:
    print(f"{img}: prédit {pred}")
    print_features(img, df_dirty)
