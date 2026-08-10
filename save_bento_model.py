import bentoml
import mlflow.sklearn

model = mlflow.sklearn.load_model("models:/wine-classifier@champion")
saved = bentoml.sklearn.save_model("wine_clf", model)
print("Salvat:", saved)
