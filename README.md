# mlops-practice

An MLOps learning project, built step by step from an empty dev environment to a full pipeline: versioned data, a trained and served model, drift monitoring, automated orchestration, and deployment to a local Kubernetes cluster.

Model used: classification on the `load_wine` dataset (scikit-learn) — chosen for simplicity, so the focus stays on infrastructure rather than model complexity.

The full process, including decisions made and problems hit along the way, is documented day by day in [`JURNAL.md`](./JURNAL.md).

## Quick Start & Reproducibility
To run the entire pipeline and services, use the provided Makefile:
1. **Build and start all services via Docker:**
   ```bash
   make up
2. **Run the pipeline tests:**
   ```bash
   make test
3. **Tear down the environment:**
   ```bash
   make clean

### Available Makefile Commands

If you want more granular control over the environment, the following commands are available:

| Command | Description |
|---|---|
| `make setup` | Sets up the local Python virtual environment and installs dependencies from `requirements.txt`. |
| `make build` | Builds the Docker image for the MLOps pipeline container. |
| `make up`    | Spins up all defined services in detached mode using Docker Compose. |
| `make test`  | Executes automated pipeline and model validation tests via `pytest`. |
| `make clean` | Stops and removes running Docker containers, freeing up system resources. |

## What this project covers

**Versioning (data + models)**
- [DVC](https://dvc.org) — dataset versioning, with a `.dvc` pointer tied to Git history
- [MLflow](https://mlflow.org) — experiment tracking (hyperparameters, metrics, artifacts) and model registry (versions + aliases, e.g. `champion`)

**Serving**
- [FastAPI](https://fastapi.tiangolo.com) — REST API with data validation (pydantic), loads the model from the registry by alias
- [Docker](https://www.docker.com) — manual containerization (`Dockerfile`, `requirements.txt`)
- [BentoML](https://www.bentoml.com) — automated packaging and containerization of the same model

**Monitoring**
- [Evidently](https://www.evidentlyai.com) — data drift detection, HTML report comparing reference vs. current distributions

**Orchestration**
- [Prefect](https://www.prefect.io) — pipeline (`pipeline.py`) with chained tasks (generate data → train → validate), automatic retries, a validation step that fails the pipeline if the model doesn't meet a minimum accuracy threshold, and a scheduled deployment (cron)

**Deployment at scale**
- [Kubernetes](https://kubernetes.io) (Minikube, local) — Deployment + Service, scaling to multiple replicas, automatic recovery when a pod fails

## Structure
```
train.py              # model training + MLflow logging
predict.py             # loads the model from the registry (by alias) and predicts
make_data.py            # generates data/wine.csv
app.py                 # FastAPI API (serves from the MLflow registry)
app_docker.py            # FastAPI variant for the container (loads model.pkl)
export_model.py           # exports the champion model as model.pkl
service.py              # BentoML service
bentofile.yaml            # BentoML build config
monitor.py              # drift report with Evidently
pipeline.py             # Prefect pipeline (orchestration)
Dockerfile              # Docker image for app_docker.py
k8s-deployment.yaml        # Kubernetes Deployment + Service
data/wine.csv.dvc          # DVC pointer to the dataset
JURNAL.md              # day-by-day learning journal
```

## Running locally (quick reference)

```bash
# environment
uv sync

# data + training + tracking
uv run python make_data.py
uv run python train.py
uv run mlflow ui              # http://127.0.0.1:5000

# serving (FastAPI)
uv run uvicorn app:app --reload     # http://127.0.0.1:8000/docs

# containerized serving (Docker)
docker build -t wine-api .
docker run -p 8000:8000 wine-api

# drift monitoring
uv run python monitor.py        # → drift_report.html

# orchestration
uv run python pipeline.py

# local Kubernetes (Minikube)
minikube start --driver=docker
minikube image load wine-api
kubectl apply -f k8s-deployment.yaml
minikube service wine-api-service --url
```

## Why this project

Built as a hands-on MLOps exercise, following a tiered roadmap (foundations → versioning/tracking → serving → orchestration → deployment at scale), with an emphasis on understanding each tool through direct use before moving to the next. Process details, including real problems encountered (Python version conflicts, WSL/Docker configuration, environment bugs) and how they were resolved, are in [`JURNAL.md`](./JURNAL.md).

## Author

**Ștefania-Alexandra Tanasă**
Robotics Engineering (English profile) — UTCN Cluj-Napoca
[GitHub](https://github.com/MasterWise23)

---

## License

MIT License — see [LICENSE](LICENSE) for details.
