VENV_NAME = .venv

.PHONY: all venv install run clean help

all: help

venv:
	python3 -m venv $(VENV_NAME)

deps:
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	python main.py

clean:
	rm -rf $(VENV_NAME)
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete

help:
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@awk 'BEGIN {FS = ":"} /^[a-zA-Z_-]+:/ {print "  " $$1}' Makefile
