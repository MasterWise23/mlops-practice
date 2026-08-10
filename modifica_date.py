import pandas as pd

df = pd.read_csv("data/wine.csv")
df_mic = df.head(89)   # păstrăm doar primele 89 de rânduri
df_mic.to_csv("data/wine.csv", index=False)
print("Date modificate —", df_mic.shape)
