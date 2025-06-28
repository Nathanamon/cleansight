import pandas as pd

# --- Config ---
CSV_CLEAN = "features_clean.csv"
CSV_DIRTY = "features_dirty.csv"

# Mets ici les fichiers ou listes des images mal classées sorties par ton test
mal_classes_clean = [
    "00217_05.jpg", "00517_04.jpg", "00543_02.jpg", "00547_06.jpg", "00566_03.jpg",
    "0e02598e-acbb-423e-912e-cf2b922b5bd7.jpeg", "3f53a459-b46f-4e87-90ac-f9e43cc23320.jpeg",
    "86cd7cf4-726f-40c5-9788-89c890be3914.jpeg", "WhatsApp Image 2020-05-09 at 2.03.37 PM (6).jpeg",
    "WhatsApp Image 2020-05-09 at 2.03.38 PM (3).jpeg", "WhatsApp Image 2020-05-09 at 2.08.14 PM.jpeg",
    "WhatsApp Image 2020-05-09 at 2.08.15 PM (2).jpeg", "WhatsApp Image 2020-05-09 at 3.57.59 PM.jpeg",
    "WhatsApp Image 2020-10-04 at 10.35.23 AM (6).jpeg"
]
mal_classes_dirty = [
    "00511_01.jpg", "00874_01.jpg", "1616.full.jpeg", "1620.full.jpeg", "2632.full.jpeg",
    "3675.jpeg", "59b578137fcbe.jpeg", "838.full.jpeg", "WhatsApp Image 2020-05-08 at 2.16.45 PM.jpeg",
    "WhatsApp Image 2020-05-08 at 2.18.57 PM (4).jpeg", "WhatsApp Image 2020-05-08 at 2.21.54 PM (1).jpeg",
    "WhatsApp Image 2020-05-08 at 2.21.56 PM (4).jpeg", "WhatsApp Image 2020-05-08 at 2.21.56 PM.jpeg",
    "WhatsApp Image 2020-05-08 at 2.39.00 PM (2).jpeg"
]

def describe_group(df, title):
    print(f"\n=== {title} ===")
    print(df.describe().T[["min", "25%", "50%", "mean", "75%", "max"]])

# --- Analyse CLEAN ---
df_clean = pd.read_csv(CSV_CLEAN, index_col=0)
df_clean_mal = df_clean.loc[mal_classes_clean]
df_clean_bien = df_clean.drop(mal_classes_clean, errors='ignore')

describe_group(df_clean_mal, "CLEAN mal classés")
describe_group(df_clean_bien, "CLEAN bien classés")

# --- Analyse DIRTY ---
df_dirty = pd.read_csv(CSV_DIRTY, index_col=0)
df_dirty_mal = df_dirty.loc[mal_classes_dirty]
df_dirty_bien = df_dirty.drop(mal_classes_dirty, errors='ignore')

describe_group(df_dirty_mal, "DIRTY mal classés")
describe_group(df_dirty_bien, "DIRTY bien classés")
