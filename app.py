from fastapi import FastAPI
from pydantic import BaseModel, Field
import mlflow.sklearn

app = FastAPI(title="Wine Classifier API")

# Modelul se încarcă O SINGURĂ DATĂ, la pornirea serverului
model = mlflow.sklearn.load_model("models:/wine-classifier@champion")

# Forma datelor de intrare: o listă de 13 numere (caracteristicile unui vin)
class Vin(BaseModel):
    features: list[float] = Field(..., min_length=13, max_length=13)

@app.get("/")
def health():
    return {"status": "API-ul merge"}

@app.post("/predict")
def predict(vin: Vin):
    predictie = model.predict([vin.features])
    return {"clasa_prezisa": int(predictie[0])}
