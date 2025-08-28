.PHONY: install test run-server run-worker lint security-check check all-checks

install:
	pip install -r requirements.txt

test:
	python manage.py test

run-server:
	python manage.py runserver 0.0.0.0:8000

run-worker:
	celery -A scout_web worker -l info

lint:
	flake8 .

security-check:
	bandit -r .

check:
	python manage.py check

all-checks: test lint security-check check
