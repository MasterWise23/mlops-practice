.PHONY: help setup build up test clean

help:
	@echo "Comenzi disponibile:"
	@echo "  make setup  - Instalează dependențele locale"
	@echo "  make build  - Construiește imaginile Docker (ex: mlops-pipeline)"
	@echo "  make up     - Pornește serviciile prin Docker Compose"
	@echo "  make test   - Rulează testele automate ale pipeline-ului"
	@echo "  make clean  - Oprește containerele și curăță resursele"

setup:
	python -m venv .venv
	.venv\Scripts\activate && pip install --upgrade pip && pip install -r requirements.txt

build:
	docker build -t mlops-pipeline .

up:
	docker compose up -d

test:
	pytest tests/

clean:
	docker compose down
