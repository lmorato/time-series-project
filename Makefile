.PHONY: help venv install

VENV=.venv
PYTHON=$(VENV)/bin/python3

help:
	@echo "Makefile targets:"
	@echo "  venv          - Create a virtual environment."
	@echo "  install       - Install dependencies."

venv:
	python3 -m venv $(VENV)

install: venv
	$(PYTHON) -m pip install -r requirements-dev.txt