setup:
	@if [ ! -f = ".env" ]; then cp .env.example .env; fi
	bash setup.sh

install:
	poetry install --with dev

test:
	poetry run pytest .

format:	
	poetry run black .

lint:
	poetry run ruff .

dev:
	poetry run python -m bin.dev

qa:
	poetry run uvicorn src.main:app --host 0.0.0.0

build:
	docker build -t python-ml-template:v0 .

run:
	docker run --cap-drop all --env-file .env -it -p 8000:8000 python-ml-template:v0

prod: build run

deploy:
	#deploy goes here

