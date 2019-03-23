.PHONY: lint
lint:
	prospector || true

.PHONY: test
test:
	pytest -v --cov-report html --cov-report term --cov=krlparser tests/
