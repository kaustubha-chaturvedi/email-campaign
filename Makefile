.PHONY: run migs wdb static celery beat shell

# Variables
MANAGE=python manage.py
HOST=0.0.0.0
PORT=8000
SETTINGS=--settings=email_campaign.settings

run:
	$(MANAGE) runserver $(HOST):$(PORT)
	
migs:
	$(MANAGE) makemigrations $(SETTINGS)
	
wdb:
	$(MANAGE) migrate $(SETTINGS)

static:
	$(MANAGE) collectstatic --noinput $(SETTINGS)

celery:
	celery -A email_campaign worker --loglevel=info

beat:
	celery -A email_campaign beat --loglevel=info

shell:
	$(MANAGE) shell $(SETTINGS)
