# Jurnal MLOps

Jurnal de învățare — progres pe zile.
Proiect: `~/mlops-practice/primul-proiect`

---

## Ziua 1 — 20 iulie 2026

### Mediu de dezvoltare
- Pornire de la WSL gol → Linux (Ubuntu) real și funcțional
- Descoperit că VS Code se conecta greșit la distribuția internă `docker-desktop` în loc de Ubuntu
- Instalat o distribuție Ubuntu reală (`wsl --install -d Ubuntu`)
- Mutat întreaga distribuție de pe C: pe E: (doar 5 GB liberi pe C:), prin export/import
- Configurat VS Code cu extensia WSL — editez în editor, execut în Linux
- Regulă reținută: codul care rulează sub Linux stă pe sistemul Linux (`/home/...`), nu pe `/mnt/c` sau `/mnt/e` (accesul cross-OS e lent)

### Unelte instalate
- Docker Desktop — pornit și funcțional (Engine running, v4.82.0)
- `uv` — manager de medii virtuale și versiuni Python (v0.11.29)
- Primul proiect structurat: folder dedicat, `.venv` izolat, dependințe în `pyproject.toml`
- Testat mediul instalând numpy

### Probleme rezolvate
- `uv init` fixase proiectul pe Python 3.14, prea nou pentru ecosistemul ML
- MLflow crăpa cu `ImportError: cannot import name 'Traversable'`
- Rezolvat: editat `requires-python` în `pyproject.toml` (3.14 → 3.12), recreat mediul cu `uv venv --python 3.12 --clear`, reinstalat pachetele cu `uv sync`
- Confirmat cu `uv run python --version` → Python 3.12.13

### MLflow — primul experiment tracking
- Scris `train.py`: antrenează un RandomForest pe setul `load_wine`
- Logat cu MLflow: hiperparametri (`n_estimators`, `max_depth`), metrica `accuracy`, modelul salvat
- Rulat cu `max_depth` diferit → rezultate: 1.000 (max_depth mare), 0.917 (max_depth=3)
- Pornit interfața web (`uv run mlflow ui` → http://127.0.0.1:5000)
- Văzut rulările în tabel; experimentul implicit se numește `Default`
- Ciclul complet: antrenează → loghează → compară

### Reflexe MLOps învățate
- Un scor perfect (accuracy 1.000) e un semnal de alarmă, nu o veste bună — prima întrebare e „ce e în neregulă?" (date scurse, set prea mic, problemă trivială)
- În ML nu se folosește cea mai nouă versiune de Python — mereu cu una-două în urmă (acum: 3.11–3.12), unde bibliotecile sunt stabile
- Un singur `Ctrl+C` pentru a opri un server, apoi răbdare — apăsat repetat, forțează întreruperea și scoate traceback-uri inofensive

---

## Ziua 2 — 21 iulie 2026

### Reluarea mediului
- Deschis Ubuntu → `cd ~/mlops-practice/primul-proiect` → `uv run mlflow ui`
- Reținut: cât timp `mlflow ui` rulează, terminalul scrie continuu linii „Waiting for child process / died" — e normal, serverul e viu, nu e eroare
- Interfața MLflow 3.14 are un comutator sus-stânga **GenAI | Model training** — rulările ML clasice sunt la „Model training" / „Training runs", nu la „GenAI" (acolo e pentru LLM-uri)

### MLflow — model registry
- Înțeles conceptul: registry = catalog separat cu modele înregistrate; fiecare are nume stabil, versiuni (v1, v2...), aliasuri și tag-uri
- Pe MLflow 3.x, vechiul sistem de „stages" (Staging/Production/Archived) e depășit din 2.9 → se folosesc **aliasuri** (ex. `champion`), mai flexibile
- Înregistrat modelul din UI: rulare → Artifacts → folder `model` → „Register Model" → nume `wine-classifier` (Version 1)
- Atribuit aliasul `champion` pe Version 1
- Scris `predict.py`: încarcă modelul după alias cu `mlflow.sklearn.load_model("models:/wine-classifier@champion")` → predicții `[0 0 0 0 0]`
- Înregistrat automat din cod: adăugat `registered_model_name="wine-classifier"` la `log_model(...)` → la rulare apare automat Version 2
- Mutat aliasul `champion` de pe v1 pe v2 (aliasul e unic — MLflow îl mută singur)
- Rulat `predict.py` NESCHIMBAT → folosește acum modelul nou; am promovat un model în producție doar mutând o etichetă

### Ideea-cheie prinsă azi
- Registry-ul decuplează „ce model rulează în producție" de codul care îl folosește: codul cere mereu `@champion`, iar cine e campion se schimbă independent

### Reflexe reținute
- La `log_model`, `artifact_path` e depășit — se va folosi `name` în viitor (deocamdată doar un warning)
- MLflow salvează și lista de dependințe (`uv export`, 93 pachete) odată cu modelul → reproductibilitate și a mediului, nu doar a fișierului

---

## Unde am rămas / Următorii pași

- Capitolul MLflow e complet: tracking (ziua 1) + registry (ziua 2)
- Toată munca e salvată în `~/mlops-practice/primul-proiect` (`train.py`, `predict.py`, `mlruns/`, config)
- Reluare: `cd ~/mlops-practice/primul-proiect`
- Următor: **nivelul 4** — Kubernetes (Minikube local) și, opțional, un cluster cloud real

---

## Roadmap unelte (ordinea de învățare)

- **Fundament:** Python + Git, Docker ✓
- **Nivel 1:** MLflow (tracking ✓ + registry ✓), DVC (versionare date) ✓
- **Nivel 2:** FastAPI ✓ + Docker ✓ + BentoML ✓, Evidently ✓ (monitorizare, drift)
- **Nivel 3:** Prefect (orchestrare) ✓
- **Nivel 4:** Kubernetes (Minikube local), platformă cloud (SageMaker / Vertex AI / Azure ML) ← *aici sunt acum*

---

## Ziua 3 — 21 iulie 2026

### Detur scurt: model serving (previzualizat, apoi amânat)
- Am aruncat un ochi pe nivelul 2 (servire model cu FastAPI), apoi am ales să revin la DVC întâi — servirea nu are sens fără reproductibilitatea completă
- Reținut: servirea = transformi modelul dintr-un script într-un API web pe care alte aplicații îl pot apela
- FastAPI + uvicorn, cu interfață de test auto-generată la `/docs` — de reluat mai târziu

### DVC — versionarea datelor
- Problema pe care o rezolvă: Git se sufocă la fișiere mari de date; DVC ține datele separat, iar în Git pune doar un pointer minuscul `.dvc`
- Instalat: `uv add dvc pandas`
- Inițializat: `uv run dvc init` (are nevoie de repo Git — exista deja din `uv init`)
- Creat `make_data.py` → a scos `load_wine` într-un fișier real `data/wine.csv` (178, 14)
- `uv run dvc add data/wine.csv` → a creat pointerul `data/wine.csv.dvc` și a pus fișierul mare în `.gitignore`
- Git: configurare per-mașină (nume + email — nu se transferă de pe alt laptop), apoi commit-ul pointerului
- Diviziunea muncii: Git urmărește pointerul, DVC urmărește datele

### Călătoria în timp cu datele (payoff-ul)
- Modificat datele (redus la 89 rânduri) → `dvc add` → commit nou
- Două commit-uri, fiecare legat de o versiune diferită de date (178 vs 89)
- `git checkout <hash-vechi> data/wine.csv.dvc` + `uv run dvc checkout` → fișierul cu 178 rânduri s-a întors
- Verificat: `(178, 14)` — datele au călătorit în timp; Git aduce pointerul, DVC aduce datele
- Igienă la final: `git checkout master data/wine.csv.dvc && uv run dvc checkout` pentru a reveni curat la ultima versiune

### Ideea-cheie prinsă azi
- Reproductibilitate completă: modele versionate (MLflow) + date versionate (DVC). Aceeași combinație cod + date + config → același rezultat, de fiecare dată
- Fiecare commit „știe" cu ce date a fost făcut

### Git — reținut
- Configurarea Git (`user.name`, `user.email`) e per-mașină/per-mediu — cea de pe alt laptop nu se transferă; se setează local
- Fiecare mediu WSL își are propriul Git și propria configurare

---

## Ziua 4 — 22 iulie 2026

### FastAPI — servirea modelului ca API
- Ideea: servirea transformă modelul dintr-un script rulat manual într-un **serviciu web** pe care orice aplicație îl poate apela prin rețea
- Instalat: `uv add fastapi uvicorn` (fastapi = cadrul în care scrii API-ul; uvicorn = serverul care îl ține pornit)
- Scris `app.py`: încarcă modelul din registry după alias (`models:/wine-classifier@champion`), endpoint `GET /` (health) și `POST /predict`
- Pornit cu `uv run uvicorn app:app --reload` → `http://127.0.0.1:8000`
- Interfață de test auto-generată la `/docs` — testezi API-ul cu mâna, fără cod de client
- Testat: vin clasa 0 → `{"clasa_prezisa": 0}`; vin clasa 1 → `{"clasa_prezisa": 1}` — modelul chiar discriminează

### Decizii de servire (nu detalii — tipare reale)
- Modelul se încarcă **o singură dată, la pornirea serverului**, nu la fiecare cerere (încărcarea e lentă)
- API-ul cere modelul după **alias**, nu după versiune → promovezi un model nou și doar repornești serverul, codul rămâne neatins
- `class Vin(BaseModel)` = contract de date; FastAPI validează automat înainte să ajungă la model

### Lecția 422 vs 500
- Trimis din greșeală `{"features": [0]}` (o singură valoare) → **500 Internal Server Error**: contractul zicea doar „listă de numere", deci a trecut de validare și a explodat în model
- Adăugat validare de formă: `features: list[float] = Field(..., min_length=13, max_length=13)` (necesită `from pydantic import BaseModel, Field`)
- Acum aceeași cerere greșită dă **422 Validation Error** cu mesaj clar
- Diferența: 422 = „am prins problema la ușă"; 500 = „a explodat înăuntru". În producție, asta e diferența dintre un API pe care se poate conta și unul care generează tichete de suport
- De reținut: validarea de formă nu garantează date *plauzibile* — 13 zerouri trec validarea, dar sunt un vin imposibil. Un API serios ar avea și limite de interval

### Docker — împachetarea API-ului
- Problema rezolvată: API-ul mergea în WSL-ul meu, cu `.venv`-ul meu. Docker îl face să ruleze **identic oriunde** — diferența dintre „merge la mine" și „merge în producție"
- Exportat modelul campion ca fișier portabil: `export_model.py` → `joblib.dump(model, "model.pkl")`
- Creat `app_docker.py` — identic cu `app.py`, dar încarcă din `model.pkl` în loc de registry
- Creat `requirements.txt` cu strict ce trebuie: fastapi, uvicorn, scikit-learn, joblib, numpy
- **Fără** mlflow, dvc, pandas — containerul de producție conține doar ce-i trebuie ca să *servească*, nu tot ce am folosit ca să antrenez
- Scris `Dockerfile` (python:3.12-slim), build: `docker build -t wine-api .`, rulare: `docker run -p 8000:8000 wine-api`
- Confirmat cu `docker ps`: imaginea `wine-api`, status Up, `0.0.0.0:8000->8000/tcp`
- Testat în `/docs` → aceeași predicție, dar venită din container

### Dockerfile — de ce în ordinea asta
- `COPY requirements.txt` + `RUN pip install` **înainte** de a copia codul → Docker memorează pașii, deci o schimbare de cod nu redeclanșează reinstalarea pachetelor (economisește minute la fiecare rebuild)
- `--host 0.0.0.0` în `CMD` e obligatoriu — fără el, uvicorn ascultă doar în interiorul containerului și nu ajungi la el din afară
- `EXPOSE 8000` declară portul; `-p 8000:8000` la rulare îl leagă de mașina gazdă

### Probleme întâmpinate
- Terminal nou → pornește în home, nu în proiect. `uv run` eșua cu „Failed to spawn: uvicorn" pentru că nu eram în folderul proiectului. **Primul lucru într-un terminal nou: `cd` în proiect**
- `NameError: name 'Field' is not defined` → import uitat. Regula: orice nume folosit trebuie importat sus
- Build Docker picat la `COPY app_docker.py` → fișierul se numea `add_docker.py` (typo). Reparat cu `mv add_docker.py app_docker.py`

### Ce am acum, cap la cap
- Model încărcat din registry → API cu validare → export ca fișier portabil → imagine Docker → container izolat care servește predicții prin rețea
- Drumul complet de la „un model antrenat" la „un serviciu care poate fi pus în producție"

---

## Ziua 5 — 23 iulie 2026

### BentoML — servirea automatizată
- Ce face: automatizează exact ce am făcut manual în ziua 4 (împachetare + servire + imagine Docker), dintr-o comandă
- Ordinea din roadmap a contat: fiindcă am scris Dockerfile-ul de mână ieri, azi văd *ce* automatizează, nu e cutie neagră
- Versiune: din 1.2 se folosește decoratorul `@bentoml.service` (sintaxa veche cu „runners" din tutorialele mai vechi nu se mai aplică)
- `save_bento_model.py`: luat modelul din registry-ul MLflow → `bentoml.sklearn.save_model("wine_clf", model)` — uneltele se leagă între ele
- `service.py` cu `@bentoml.service` + `@bentoml.api`; modelul se încarcă în `__init__`
- Tipurile Python (`list[float]` → `dict`) devin automat contractul API-ului — rolul pe care-l juca `class Vin` cu pydantic
- Pornit: `uv run bentoml serve service:WineClassifier` → **portul 3000** (nu 8000 ca la FastAPI)

### BentoML — build + containerize (payoff-ul)
- `bentofile.yaml` — 7 linii, față de `requirements.txt` + `Dockerfile` + `app_docker.py` + `export_model.py` de ieri
- Nu trebuie specificat manual: copierea modelului (îl știe din `model_ref`), comanda de pornire, `--host 0.0.0.0`, `EXPOSE`
- `uv run bentoml build` → un „Bento" = cod + model + dependințe + metadate, versionat automat
- `uv run bentoml containerize wine_classifier:latest` → **generează singur Dockerfile-ul** și construiește imaginea
- Rulat containerul, testat cu același vin → aceeași predicție, fără nicio linie de Dockerfile scrisă de mine

### Evidently — monitorizare și data drift
- Închide bucla din diagrama primei zile: Date → Antrenare → Deploy → **Monitorizare** → înapoi la Date
- Versiune: importurile moderne sunt `from evidently import Report` și `from evidently.presets import DataDriftPreset` (varianta cu `evidently.report` / `evidently.metric_preset` e pentru ≤0.6.7)
- `monitor.py`: referință = primele 89 rânduri, curent = ultimele 89 → în `load_wine` vinurile sunt ordonate pe clase, deci drift real, nu fabricat
- `snapshot.save_html("drift_report.html")`, deschis cu `explorer.exe .` din WSL
- Rezultat: **13 din 14 coloane au driftat**, pondere 0.929, peste pragul 0.5 → drift la nivel de set
- Sub capotă: teste statistice (Kolmogorov-Smirnov pentru numerice, chi-pătrat pentru categorice) — compară forma întregii distribuții, nu doar mediile

### Capcana „Drift Score" (de reținut!)
- Coloana „Drift Score" NU e „cât de mult a driftat" — e **p-value-ul** testului statistic
- Scor **mic** = dovadă **puternică** de drift (prag uzual 0.05)
- Exemplu din raportul meu: `color_intensity` scor 0.0138 → drift **detectat**; `ash` scor 0.63 → drift **nedetectat**
- Pare pe dos la prima citire — e o capcană clasică

### Alte observații din raport
- `ash` e singura coloană fără drift: conținutul de cenușă e cam același indiferent de tipul de vin. Drift-ul nu e totul-sau-nimic, se întâmplă pe caracteristici individuale — raportul îți spune *unde* s-a schimbat lumea
- Au fost 14 coloane, dar modelul folosește 13 caracteristici: a 14-a e **target**-ul, și a driftat și el
- Drift pe target = schimbarea distribuției etichetelor, semnalul cel mai grav în producție: însăși problema s-a schimbat, nu doar intrările

### Bilanț — nivelul 2 complet
- Lanț MLOps funcțional cap-la-cap în 5 zile: date versionate (DVC) → experimente și modele versionate (MLflow) → model servit ca API (FastAPI) → containerizat manual (Docker) și automat (BentoML) → monitorizat pentru drift (Evidently)

---

## Ziua 6 — 10 august 2026

### Publicarea proiectului pe GitHub
- Verificat `git status` — multe fișiere „grele" riscau să ajungă pe GitHub (mlruns/, model.pkl, mlflow.db, .bentoml/) — trebuiau excluse
- Reparat `.gitignore`: un lipit incomplet în nano lăsase fișierul trunchiat la jumătate (se oprea la `.venv`); completat cu liniile lipsă
- Decizie: `JURNAL.md` rămâne urmărit (dovadă de proces pentru CV), `drift_report.html` intră în `.gitignore` (fișier generat, nu cod sursă)
- Git nu era configurat pe acest laptop — normal, configurarea (`user.name`/`user.email`) e per-mașină, nu se transferă de pe alt laptop
- Creat repo pe GitHub, legat cu `git remote add origin` + `git push -u origin main`
- Autentificare: parola de cont nu mai e acceptată de GitHub din 2021 — generat un **Personal Access Token** (scope `repo`) și folosit ca parolă la push
- Proiect live: github.com/MasterWise23/mlops-practice

### Prefect — orchestrare (nivelul 3)
- Ideea: până acum scripturile rulau manual, în ordine; orchestrarea le leagă într-un **pipeline** care rulează singur și e vizibil într-un dashboard
- Ales Prefect (mai prietenos ca prim contact decât Airflow, standardul de industrie dar mai greoi) — conceptele se transferă
- `@task` = un pas individual; `@flow` = pipeline-ul care le cheamă în ordine
- Scris `pipeline.py`: task-uri `genereaza_date`, `antreneaza` (cu `retries=2, retry_delay_seconds=5`), `valideaza` (oprește pipeline-ul dacă accuracy sub un prag)
- Rulat local (`uv run python pipeline.py`) — vizibil în dashboard-ul Prefect (`prefect server start`, port **4200**, diferit de MLflow/5000 și BentoML/3000)
- Testat un eșec controlat (prag imposibil de atins) → pipeline-ul s-a oprit exact la task-ul `valideaza`, cu eroarea vizibilă atât în terminal cât și în dashboard (rulare marcată „Failed", cu motivul exact)
- Diferența-cheie față de scripturi separate: eșecul nu se pierde tăcut într-un terminal închis — rămâne înregistrat, cu cauza la un click distanță

### Prefect — deployment programat
- `.serve()` cu `cron="0 6 * * *"` — cea mai simplă cale de a programa un flow, fără worker/infrastructură separată
- Deployment vizibil în dashboard la secțiunea „Deployments", cu programul afișat și buton „Run" pentru declanșare manuală imediată
- Testat cu „Run" manual — a pornit o rulare nouă, vizibilă în istoric
- De reținut: programul (cron) e activ doar cât timp scriptul cu `.serve()` rulează activ — pentru rulare 24/7 reală ar trebui infrastructură suplimentară (worker persistent), dincolo de scopul exercițiului

### Bilanț — nivelul 3 complet
- Pipeline cu task-uri legate, retry automat, validare care oprește flow-ul dacă modelul nu e suficient de bun, programare automată — sistemul mic al unei echipe reale: „antrenează → verifică dacă e suficient de bun → doar dacă da, mergi mai departe"
- Decizie: se continuă și cu **nivelul 4** (Kubernetes / cloud) — găsite joburi care îl cer explicit
