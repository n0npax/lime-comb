EXECUTABLES := poetry black
K := $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.PHONY: lint
lint:
	poetry run black .
	isort $(shell find . -name "*.py") -qy
	bandit -r . -x $(shell find . -name "test_*.py" | tr "\n" ",")

cover: test
	bash <(curl -s https://codecov.io/bash) -cF python

.PHONY: test
test:
	poetry run pytest -v --cov-report=xml --cov . .

.PHONY: build
build: test
	poetry build

.PHONY: clean
clean:
	find . -name __pycache__ | xargs rm -fr
	find . -name '*.pyc' -delete

.PHONY: install
install:
	echo TODO
