.PHONY: all clean

all: install lint test ufc-raw-data.csv

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
	@$(RM) ufc-raw-data.csv


data/ufc-raw-data.csv: ufc_scraping/data_script.py ufc_scraping/ufc_scraping.py
	poetry run python ufc_scraping/data_script.py