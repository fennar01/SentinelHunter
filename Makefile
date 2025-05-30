# Makefile for SentinelHunter

.PHONY: build test sim lint gui

build:
	@echo "Building all components..."
	# Add build commands for C++, Python, JS

lint:
	@echo "Linting all code..."
	pre-commit run --all-files || true

sim:
	docker build -t sentinel-sim ./sim
	docker run --rm sentinel-sim

test:
	@echo "Running all tests..."
	# Add test commands for C++, Python, JS

# GUI (React/Electron)
gui:
	@echo "Starting GUI..."
	# Add GUI start command (placeholder)
