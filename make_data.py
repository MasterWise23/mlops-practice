from sklearn.datasets import load_wine
import pandas as pd
import os

# Ia setul de vinuri ca tabel
date = load_wine(as_frame=True).frame

# Salvează-l ca fișier CSV, într-un folder data/
os.makedirs("data", exist_ok=True)
date.to_csv("data/wine.csv", index=False)

print("Salvat:", date.shape, "→ data/wine.csv")

