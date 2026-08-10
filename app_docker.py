from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib

app = FastAPI(title="Wine Classifier API")
model = joblib.load("model.pkl")

class Vin(BaseModel):
    features: list[float] = Field(..., min_length=13, max_length=13)

@app.get("/")
def health():
    return {"status": "API-ul merge"}

@app.post("/predict")
def predict(vin: Vin):
    predictie = model.predict([vin.features])
    return {"clasa_prezisa": int(predictie[0])}
