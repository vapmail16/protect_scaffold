install:
	poetry install

test:
	poetry run pytest tests/

lint:
	poetry run flake8 src/

run:
	poetry run python src/main.py

format:
	poetry run black src/ tests/

check:
	poetry run mypy src/

clean:
	poetry env remove python

build:
	poetry build

publish:
	poetry publish 