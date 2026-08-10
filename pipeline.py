from prefect import task, flow
import pandas as pd
from sklearn.datasets import load_wine
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import mlflow
import mlflow.sklearn
import os


@task
def genereaza_date():
    os.makedirs("data", exist_ok=True)
    df = load_wine(as_frame=True).frame
    df.to_csv("data/wine.csv", index=False)
    return "data/wine.csv"


@task(retries=2, retry_delay_seconds=5)
def antreneaza(cale_date: str, max_depth: int = 5):
    df = pd.read_csv(cale_date)
    X = df.drop(columns=["target"])
    y = df["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    with mlflow.start_run():
        model = RandomForestClassifier(max_depth=max_depth, random_state=42)
        model.fit(X_train, y_train)
        acc = accuracy_score(y_test, model.predict(X_test))

        mlflow.log_param("max_depth", max_depth)
        mlflow.log_metric("accuracy", acc)
        mlflow.sklearn.log_model(
            model, "model", registered_model_name="wine-classifier"
        )
    return acc


@task
def valideaza(acc: float, prag_minim: float = 0.7):
    if acc < prag_minim:
        raise ValueError(f"Accuracy {acc:.3f} sub pragul minim {prag_minim}")
    print(f"Validare trecuta — accuracy {acc:.3f} >= {prag_minim}")
    return True


@flow(name="pipeline-antrenare-vin")
def pipeline_antrenare(max_depth: int = 5, prag_minim: float = 0.7):
    cale = genereaza_date()
    acc = antreneaza(cale, max_depth)
    valideaza(acc, prag_minim)
    print(f"Pipeline terminat — accuracy: {acc:.3f}")
    return acc


if __name__ == "__main__":
    pipeline_antrenare.serve(
        name="pipeline-vin-zilnic",
        cron="0 6 * * *", #in fiecare zi la ora 06:00
        parameters={"max_depth":5, "prag_minim":0.7},
)
