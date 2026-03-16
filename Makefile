.PHONY: check-format check-format-diff format lint

check-format:
	poetry run black --check --color .
	poetry run isort --check --color .

check-format-diff:
	poetry run black --check --diff --color .
	poetry run isort --check --diff --color .

format:
	poetry run black --color .
	poetry run isort --color .

lint:
	poetry run pylint bluetooth_mesh tests --exit-zero --output-format=colorized
