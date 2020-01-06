EXECUTABLES := poetry curl
K := $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.PHONY: deps
deps:
	poetry install

.PHONY: lint
lint: deps
	poetry run black .
	isort $(shell find . -name "*.py") -qy
	bandit -r . -x $(shell find . -name "test_*.py" | tr "\n" ",")

# make test CI=true
cover: test
	curl -s https://codecov.io/bash -o codecov_upload.sh
ifdef CI
	bash codecov_upload.sh -cF cli
else
	bash codecov_upload.sh -cF cli -t $(shell cat .codecov_token)
endif


.PHONY: test
test: deps
	poetry run pytest -v --cov-report=xml --cov . .

.PHONY: build
build: deps clean test cover lint
	poetry build

.PHONY: clean
clean:
	rm -fr dist
	rm -fr cli.egg-info
	find . -name __pycache__ | xargs rm -fr
	find . -name '*.pyc' -delete

.PHONY: install
install:
	echo TODO

.PHONY: release
release: build
ifdef BUMP
	poetry version $(BUMP)
endif
	$(MAKE) build
	poetry version | awk '{print $$NF}' | xargs git tag -f
	git push --tags
	echo TODO release to pypi

