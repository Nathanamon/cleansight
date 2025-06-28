import os

DIR = "../../Data/train/with_label/dirty"

removed = 0
for f in os.listdir(DIR):
    if "_resized" in f or "_compressed" in f:
        os.remove(os.path.join(DIR, f))
        removed += 1

print(f"✅ {removed} fichiers '_resized' ou '_compressed' supprimés dans {DIR}")
