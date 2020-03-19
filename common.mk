EXECUTABLES := poetry curl isort bandit
K := $(foreach exec,$(EXECUTABLES),\
        $(if $(shell which $(exec)),some string,$(error "No $(exec) in PATH")))

.PHONY: deps
deps: requirements.txt
	poetry install --no-root

.PHONY: lint
lint:
	sed -i 's/[ \t]*$$//' $(shell find . -name "*.md")
	sed -i 's/[ \t]*$$//' $(shell find . -name "*.py")
	isort $(shell find . -name "*.py") -qy
	bandit -r . -x $(shell find . -name "test_*.py" | tr "\n" ",")
	poetry run black .

cover: test codecov_upload.sh
ifeq ("$(wildcard .codecov_token)","")
	./codecov_upload.sh -cF cli -t "$${CODECOV_TOKEN}" -C "$${COMMIT_SHA}" -Z
else
	./codecov_upload.sh -cF cli -t "$(shell cat .codecov_token)" -Z
endif


.PHONY: test
test: deps 
	poetry run pytest -vs --cov-report=xml --cov . .


.PHONY: update_version
update_version:
	sed -i 's/__version__.*/__version__ = "$(shell poetry version | cut -f2 -d " ")"/g' lime_comb/__init__.py

.PHONY: build
build:  update_version deps clean test cover lint
	poetry $@

.PHONY: clean
clean:
	rm -fr dist
	rm -fr cli.egg-info
	find . -name __pycache__ | xargs rm -fr
	find . -name '*.pyc' -delete
	rm $${HOME}/.config/lime-comb/ -fr || true
	rm $${HOME}/.local/share/lime-comb/ -fr || true

.PHONY: install
install:
	poetry build
	pip3 uninstall -y lime-comb-cli
	pip3 $@ dist/*.whl

.PHONY: release
release: build
ifeq ("$(wildcard .codecov_token)","")
	poetry publish -u '__token__' -p "$${PYPI_TOKEN}" || true
else
	poetry publish -u '__token__' -p "$(shell cat .pypi_token)"
endif

codecov_upload.sh:
	curl -s https://codecov.io/bash -o codecov_upload.sh
	chmod +x ./codecov_upload.sh

.PHONY: requirements-dev.txt
requirements-dev.txt:
	echo $(shell poetry export -f requirements.txt --without-hashes > requirements-dev.txt)

.PHONY: requirements.txt
requirements.txt:
	echo $(shell poetry export -f requirements.txt --dev --without-hashes > requirements.txt)
