MANAGEPY = src/manage.py
help:
	@echo 'Usage:'
	@echo '   make migrate'
	@echo '   make run'
	@echo 'Development: '
	@echo '   make test        run unit and integration tests'
	@echo '   make mypy        run mypy static typing checker'
	@echo '   make buidl       run linters and tests'

build: mypy test

run:
	$(MANAGEPY) runserver

test:
	PYTHONPATH=src/:./ pytest

migrate:
	$(MANAGEPY) makemigrations && $(MANAGEPY) migrate