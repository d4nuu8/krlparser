.PHONY: lint
lint:
	prospector || true

.PHONY: test
test:
	coverage run -m unittest
	coverage html --omit="tests*/"
	coverage report --omit="tests*/"
