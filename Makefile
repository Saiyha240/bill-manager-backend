.DEFAULT_GOAL := default

migrate:
	python manage.py makemigrations; \
    python manage.py migrate

install-dev:
	pip install -r requirements/development.txt

serve:
	python manage.py runserver

default: install-dev
