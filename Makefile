.PHONY: docs


init:
	pip install -r requirements.txt

test:
	py.test

install:
	python setup.py install

docs:
	cd docs && make html
	@echo "\033[95m\n\nBuild successful! View the docs homepage at docs/_build/html/index.html.\n\033[0m"

clean:
	cd docs && make clean

