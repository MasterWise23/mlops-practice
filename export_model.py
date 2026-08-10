import mlflow.sklearn
import joblib

model = mlflow.sklearn.load_model("models:/wine-classifier@champion")
joblib.dump(model, "model.pkl")
print("Model exportat în model.pkl")
