.PHONY: venv lint-check install run

venv:
	python -m venv venv

install:
	pip install -r requirements.txt
	pip install ruff mypy

lint-check:
	ruff check app/
	mypy app/ --ignore-missing-imports

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

