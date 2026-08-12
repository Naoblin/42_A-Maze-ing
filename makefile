MYPY_FLAGS = --warn-return-any --warn-unused-ignores \
    --ignore-missing-imports --disallow-untyped-defs \
    --check-untyped-defs

.PHONY: install run debug clean lint lint-strict

run:
	python3 a_maze_ing.py config.txt

install:
	pip install mazegen-1.0.0-py3-none-any.whl

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +

lint:
	-flake8 .
	python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	-flake8 .
	python3 -m mypy . --strict