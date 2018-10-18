.PHONY: lint
lint:
	pylint krlparser tests || true

.PHONY: test
test:
	coverage run -m unittest
	coverage html --omit="tests*/"
	coverage report --omit="tests*/"
