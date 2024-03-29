APPLICATION_NAME = auth
CODE = $(APPLICATION_NAME)

# Commands
env:  ##@Environment Create .env file with variables
	@$(eval SHELL:=/bin/bash)
	@cp .env.example .env
	@echo "SECRET_KEY=$$(openssl rand -hex 32)" >> .env

lint:  ##@Code Check code with pylint
	poetry run python3 -m pylint $(CODE)

format:  ##@Code Reformat code with isort and black
	poetry run python3 -m isort $(CODE)
	poetry run python3 -m black $(CODE)

db:  ##@Database Create database with docker-compose
	docker compose -f docker-compose.yml up -d --remove-orphans

revision:
	alembic revision --autogenerate -m "$(name)"

migrate:  ##@Database Do all migrations in database
	poetry run alembic upgrade head

run:  ##@Application Run application server
	poetry run python3 -m $(APPLICATION_NAME)