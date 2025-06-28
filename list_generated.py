import os

DIR = "Data/train/with_label/clean"

fichiers = [f for f in os.listdir(DIR) if '_resized' in f or '_compressed' in f]
print("Fichiers générés détectés :")
for f in fichiers:
    print(f)

print(f"\nTotal fichiers générés trouvés : {len(fichiers)}")
