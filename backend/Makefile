PM = python manage.py

run:
	$(PM) runserver


migrates: migrations migrate ;


migrations:
	$(PM) makemigrations


migrate:
	$(PM) migrate


superuser:
	$(PM) createsuperuser



.PHONY: all run migrations migrate migrates
