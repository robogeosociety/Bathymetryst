.PHONY: help setup data fetch model manifest serve clean

PY ?= python3
VENV := .venv
VENV_PY := $(VENV)/bin/python
PORT ?= 8000

help:
	@echo "Bathymetryst targets:"
	@echo "  make setup     create venv and install requirements"
	@echo "  make data      fetch -> model -> manifest (full pipeline)"
	@echo "  make manifest  rebuild web/data/manifest.json from the sea-level curve"
	@echo "  make serve     serve web/ at http://localhost:$(PORT)"
	@echo "  make clean      remove generated data and caches"

setup:
	$(PY) -m venv $(VENV)
	$(VENV_PY) -m pip install --upgrade pip
	$(VENV_PY) -m pip install -r requirements.txt

# Full pipeline. fetch/model are stubs today; manifest runs on the seed curve.
data: fetch model manifest

fetch:
	-$(VENV_PY) -m pipeline.fetch_dem
	-$(VENV_PY) -m pipeline.fetch_basemap

model:
	-$(VENV_PY) -m pipeline.model_shoreline

# manifest uses stdlib only, so run with system python if no venv yet.
manifest:
	$(PY) -m pipeline.build_manifest

serve:
	cd web && $(PY) -m http.server $(PORT)

clean:
	rm -rf data/raw/* data/processed/* __pycache__ pipeline/__pycache__
