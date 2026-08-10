import bentoml
import numpy as np

@bentoml.service(name="wine_classifier")
class WineClassifier:
    model_ref = bentoml.models.BentoModel("wine_clf:latest")

    def __init__(self):
        self.model = bentoml.sklearn.load_model(self.model_ref)

    @bentoml.api
    def predict(self, features: list[float]) -> dict:
        predictie = self.model.predict(np.array([features]))
        return {"clasa_prezisa": int(predictie[0])}
