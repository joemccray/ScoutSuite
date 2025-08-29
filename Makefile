.PHONY: install test run-server run-worker lint security-check check all-checks

install:
	pip install -r requirements.txt

test:
	python src/manage.py test scout_web

run-server:
	python src/manage.py runserver 0.0.0.0:8000

run-worker:
	PYTHONPATH=src celery -A scout_web worker -l info

lint:
	flake8 .

security-check:
	bandit -r .

check:
	python src/manage.py check

all-checks: test lint security-check check
