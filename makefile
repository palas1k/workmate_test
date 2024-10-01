PORT:=3000
PYTHONPATH=./
CONFIG_PATH=./deploy/config.toml

run:
	CONFIG_PATH=./deploy/config.toml PYTHONPATH=./ poetry run python src/main

dev:
	docker compose -f ./docker-compose.yaml up --build -d

migrate:
	alembic upgrade head

test:
	pytest