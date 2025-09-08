# Darwin - Genetic Algorithm Evolution Simulator
# Makefile for project management

.PHONY: help venv deps run test clean reports

# Python interpreter
PYTHON := .venv/bin/python
PIP := .venv/bin/pip

help: ## show help message
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)

venv: ## create virtual environment
	python3 -m venv .venv

deps: ## install dependencies
	$(PIP) install --upgrade pygame numpy matplotlib

run: ## run simulation (GUI)
	$(PYTHON) main.py

test: ## Run tests (placeholder for future implementation)
	@echo "Tests not yet implemented"

clean: ## Clean up temporary files
	find . -type d -name "__pycache__" -delete

reports: ## Open reports directory
	@if [ -d "reports" ]; then \
		open reports/; \
	else \
		echo "No reports directory found. Run a simulation first."; \
	fi
