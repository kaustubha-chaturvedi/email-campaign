.PHONY: run migs wdb

run:
	@python manage.py runserver

migs:
	@python manage.py makemigrations

wdb:
	@python manage.py migrate
