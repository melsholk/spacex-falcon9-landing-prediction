.PHONY: help install dev test lint make-dataset train run-dashboard

help:
	@echo "Common targets:"
	@echo "  make install       - install runtime deps + package"
	@echo "  make dev           - install dev deps"
	@echo "  make lint          - run ruff"
	@echo "  make test          - run pytest"
	@echo "  make make-dataset  - collect minimal dataset from SpaceX API"
	@echo "  make train         - train best model (expects data/processed/model_table.csv)"
	@echo "  make run-dashboard - run Dash app (expects data/raw/spacex_launch_dash.csv)"

install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	pip install -e .

dev: install
	pip install -r requirements-dev.txt

lint:
	ruff check .

test:
	pytest -q

make-dataset:
	python scripts/make_dataset.py --out data/processed/dataset.csv

train:
	python scripts/train_model.py --data data/processed/model_table.csv --model_out models/best_model.joblib

run-dashboard:
	python -m spacex_landing.dashboard.app --data data/raw/spacex_launch_dash.csv
