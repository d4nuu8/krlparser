.PHONY: lint
lint:
	pylint -j 0 krllint tests --output-format=colorized

.PHONY: test
test:
	python -m unittest
