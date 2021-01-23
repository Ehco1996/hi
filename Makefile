.PHONY: setup update fmt publish

setup:
	poetry install

update:
	poetry update

publish:
	poetry build && poetry publish

fmt:
	autoflake --recursive --remove-all-unused-imports --in-place . && isort . && black .
