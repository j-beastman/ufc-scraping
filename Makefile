.PHONY: all clean

all: install lint test box_office_and_video.csv

install:
	poetry install

test:
	poetry run pytest
 
format:
	poetry run isort .
	poetry run black .
	poetry run autopep8 --in-place --aggressive --aggressive --recursive .
	make lint

lint:
	poetry run isort --check .
	poetry run black --check .
	poetry run flake8
	#poetry run pycodestyle
	#poetry run pylint boxofficepredictor

clean:
	@$(RM) example.csv

##example.csv: boxofficepredictor/box_office.py
##	poetry run python boxofficepredictor/box_office.py