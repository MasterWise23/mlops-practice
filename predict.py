import mlflow.sklearn
from sklearn.datasets import load_wine

# Cere modelul după ALIAS, nu după număr de versiune
model = mlflow.sklearn.load_model("models:/wine-classifier@champion")

X, _ = load_wine(return_X_y=True)
predictii = model.predict(X[:5])

print("Predicții pentru primele 5 vinuri:", predictii)