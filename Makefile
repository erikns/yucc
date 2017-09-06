.PHONY: develop dist upload-test

develop:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@test ${VIRTUAL_ENV} || (echo "Use a virtual environment for development setup" && exit 1)
	pip install -e .

dist:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@rm -rf dist
	@python setup.py sdist

upload-test:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@twine upload --repository-url https://test.pypi.org/legacy/ dist/*

upload-production:
	@test -f README.md || (echo "Run make from root project directory!" && exit 1)
	@twine upload --repository-url https://pypi.python.org/pypi/ dist/*
