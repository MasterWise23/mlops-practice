import mlflow
import mlflow.sklearn
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 1. Datele (un set clasic: clasificare de vinuri)
X, y = load_wine(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 2. Hiperparametrii — pe ăștia îi vei schimba între rulări
n_estimators = 100
max_depth = 5

# 3. O rulare MLflow
with mlflow.start_run():
    model = RandomForestClassifier(
        n_estimators=n_estimators, max_depth=max_depth, random_state=42
    )
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    acc = accuracy_score(y_test, preds)

    # 4. Loghează ce ai făcut și ce a ieșit
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("max_depth", max_depth)
    mlflow.log_metric("accuracy", acc)
    mlflow.sklearn.log_model(model, "model", registered_model_name="wine-classifier")

    print(f"Rulare gata — accuracy: {acc:.3f}")
