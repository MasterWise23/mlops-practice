import pandas as pd
from evidently import Report
from evidently.presets import DataDriftPreset

df = pd.read_csv("data/wine.csv")

# Simulăm două momente în timp:
reference = df.head(89)   # datele pe care "am antrenat" modelul
current = df.tail(89)     # datele care "vin acum din producție"

report = Report(metrics=[DataDriftPreset()])
snapshot = report.run(reference_data=reference, current_data=current)
snapshot.save_html("drift_report.html")

print("Raport salvat în drift_report.html")
