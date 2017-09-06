.PHONY: develop dist upload

TWINE_ENV ?= test
include ~/.twinevars.${TWINE_ENV}
export $(shell sed 's/=.*//' ~/.twinevars.${TWINE_ENV})

develop:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@test ${VIRTUAL_ENV} || (echo "Use a virtual environment for development setup" && exit 1)
	pip install -e .

dist:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@rm -rf dist
	@python setup.py sdist

upload:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@echo "Uploading to repository: ${TWINE_REPOSITORY_URL}..."
	@twine upload --repository-url ${TWINE_REPOSITORY_URL} -u ${TWINE_USERNAME} -p ${TWINE_PASSWORD} dist/*
