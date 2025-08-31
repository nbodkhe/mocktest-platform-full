.PHONY: run up down fmt test
run:
	uvicorn app.main:app --reload
up:
	docker compose up --build
down:
	docker compose down -v
fmt:
	python -m black app
test:
	pytest -q
