# Darwin - Genetic Algorithm Evolution Simulator
# Makefile for project management

.PHONY: help install run clean test format lint setup

# Python interpreter
PYTHON := .venv/bin/python
PIP := .venv/bin/pip

# Default target
help:
	@echo "Darwin Project - Makefile Commands"
	@echo "=================================="
	@echo "setup     - Setup virtual environment and install dependencies"
	@echo "install   - Install/update dependencies"
	@echo "run       - Run the Darwin simulation"
	@echo "test      - Run tests (when implemented)"
	@echo "format    - Format code with black (when installed)"
	@echo "lint      - Lint code with flake8 (when installed)"
	@echo "clean     - Clean up temporary files"
	@echo "reports   - Open reports directory"
	@echo "help      - Show this help message"

# Setup virtual environment and install dependencies
setup:
	@echo "Setting up Darwin project..."
	python3 -m venv .venv
	$(PIP) install --upgrade pip
	$(PIP) install pygame numpy matplotlib
	@echo "Setup complete! Run 'make run' to start the simulation."

# Install/update dependencies
install:
	$(PIP) install --upgrade pygame numpy matplotlib

# Run the Darwin simulation
run:
	$(PYTHON) main.py

# Run tests (placeholder for future implementation)
test:
	@echo "Tests not yet implemented"

# Format code (if black is installed)
format:
	@if command -v black >/dev/null 2>&1; then \
		black src/ main.py; \
	else \
		echo "Black not installed. Run: pip install black"; \
	fi

# Lint code (if flake8 is installed)
lint:
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 src/ main.py; \
	else \
		echo "Flake8 not installed. Run: pip install flake8"; \
	fi

# Clean up temporary files
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .pytest_cache/
	rm -rf build/
	rm -rf dist/

# Open reports directory
reports:
	@if [ -d "reports" ]; then \
		open reports/; \
	else \
		echo "No reports directory found. Run a simulation first."; \
	fi

# Development setup with additional tools
dev-setup: setup
	$(PIP) install black flake8 pytest
	@echo "Development environment setup complete!"
