MYPY_FLAGS = --warn-return-any --warn-unused-ignores \\
	--ignore-missing-imports --disallow-untyped-defs \\
	--check-untyped-defs

.PHONY: install run debug clean lint lint-strict

install:
	pip install -r requirements.txt

run:
	python3 a_maze_ing.py config.txt

debug:
	python3 -m pdb a_maze_ing.py config.txt

clean:
	rm -rf __pycache__ .mypy_cache
# 	Nize je prikaz, ktery navrhnulo AI. Az uvidime, jake soubory
# 	se nam generuji, tak bych prikaz vysle pripadne upravil
# 	rm -rf __pycache__ .mypy_cache build dist *.egg-info

lint:
	flake8 .
	python3 -m mypy . $(MYPY_FLAGS)

lint-strict:
	flake8 .
	python3 -m mypy . --strict