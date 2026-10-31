.PHONY: up down logs ps test test-backend test-frontend lint e2e migrate sdk sde fmt adr

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f --tail=100

ps:
	docker compose ps

test: test-backend test-frontend

test-backend:
	cd backend && uv run pytest

test-frontend:
	cd frontend && npm test

lint:
	cd backend && uv run ruff check . && uv run ruff format --check .
	cd frontend && npm run lint

fmt:
	cd backend && uv run ruff format .
	cd frontend && npx prettier --write "src/**/*.{ts,tsx,css}"

e2e:
	cd frontend && npx playwright test

migrate:
	docker compose exec backend uv run alembic upgrade head

sdk:
	cd backend && PYTHONPATH=src uv run python -c "import json,sys;from app.main import app;json.dump(app.openapi(), sys.stdout)" > /tmp/occc-openapi.json
	cd frontend && npx openapi-typescript /tmp/occc-openapi.json -o src/api/schema.d.ts

sde:
	docker compose exec backend uv run python -m app.sde.download

adr:
	npx -y @adrkit/cli lint
