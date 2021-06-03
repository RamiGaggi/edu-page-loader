install:
	poetry install

build:
	poetry build

test:
	poetry run pytest -vv tests

test-coverage:
	poetry run pytest --cov=hexlet_python_package --cov-report xml

package-install:
	python3 -m pip install --user --force-reinstall dist/*.whl

publish:
	poetry publish --dry-run
	
lint:
	poetry run flake8 page_loader