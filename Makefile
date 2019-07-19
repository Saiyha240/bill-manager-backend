.DEFAULT_GOAL := default

create-superuser:
	python manage.py createsuperuser --email admin@example.com --username admin --first_name '' --last_name ''
migrate:
	python manage.py makemigrations; \
    python manage.py migrate

install-dev:
	pip install -r requirements/development.txt

serve:
	python manage.py runserver

default: install-dev
