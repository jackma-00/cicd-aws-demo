.PHONY: venv install format lint test local_launch

venv:
	python3 -m venv .venv

install: setup.py
	. ./.venv/bin/activate && \
	pip install --upgrade pip &&\
	pip install .[dev]

format:
	. ./.venv/bin/activate && \
	black .

lint: venv install
	. ./.venv/bin/activate && \
	black --check . && \
	pylint -j 0 --disable=C,W ./src/

test: venv install
	. ./.venv/bin/activate && \
	pytest .

local_launch: venv install
	. .venv/bin/activate && \
	uvicorn --port 8080 --reload src.main:app