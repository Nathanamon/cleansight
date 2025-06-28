import pandas as pd

df_clean = pd.read_csv("features_clean.csv")
df_dirty = pd.read_csv("features_dirty.csv")

print("== CLEAN ==")
print(df_clean.describe())
print("\n== DIRTY ==")
print(df_dirty.describe())

