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

cover: test codecov_upload.sh
ifeq ("$(wildcard .codecov_token)","")
	./codecov_upload.sh -cF cli -t "$${CODECOV_TOKEN}" -C "$${COMMIT_SHA}" -Z
else
	./codecov_upload.sh -cF cli -t "$(shell cat .codecov_token)" -Z
endif


.PHONY: test
test: deps 
	firebase emulators:start --only firestore &
	sleep 5
	poetry run pytest -v --cov-report=xml --cov . .
	$(MAKE) firestore-stop

firestore-stop:
	pgrep -lfa firebase | grep -v -e make | cut -f1 -d ' ' | xargs -n1 kill -9

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
	poetry install

.PHONY: release
release:
	$(MAKE) build
	echo TODO release to pypi

codecov_upload.sh:
	curl -s https://codecov.io/bash -o codecov_upload.sh
	chmod +x ./codecov_upload.sh
