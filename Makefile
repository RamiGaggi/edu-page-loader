install:
	@poetry install

build:
	@poetry build

test:
	@poetry run pytest --log-cli-level=INFO -vv tests

test-coverage:
	@poetry run pytest --cov=page_loader --cov-report xml

package-install: build
	@python3 -m pip install --user --force-reinstall dist/*.whl

publish:
	@poetry publish --dry-run
	
lint:
	@poetry run flake8 page_loader