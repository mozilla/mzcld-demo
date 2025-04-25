.PHONY: run build start-container start-collector load-test

ifneq (,$(wildcard ./.env))
    include .env
    export
endif

current_dir := $(shell basename $(CURDIR))

build:
	docker compose build

run:
	docker compose up

lint:
	docker compose run --rm app shell ruff format --check
	docker compose run --rm app shell ruff check

test:
	docker compose run --rm web shell /app/script/test.sh

start-container:
	docker run -d -p 8000:8000 --rm $(current_dir):latest

start-collector:
	docker run \
		--name otel-collector \
		-d \
		-p 4317:4317 -p 4318:4318 -p 8889:8889 --rm \
		-v ./collector-config.yaml:/etc/otelcol-config.yaml \
		otel/opentelemetry-collector-contrib:latest \
		--config /etc/otelcol-config.yaml

load-test:
	k6 --vus 20 --duration 30s run ./k6-script.js

