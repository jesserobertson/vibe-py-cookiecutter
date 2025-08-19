# Makefile for cookiecutter template testing

# Makefile for cookiecutter template testing (using unified scripts)

.PHONY: help install test test-fast test-integration test-slow clean lint format

help:
	@echo "Available commands (using unified scripts):"
	@echo "  install       - Install test dependencies"
	@echo "  test          - Run all tests"
	@echo "  test-fast     - Run fast tests only (skip integration/slow)"
	@echo "  test-integration - Run integration tests"
	@echo "  test-slow     - Run slow tests"
	@echo "  test-generation - Run cookiecutter generation tests"
	@echo "  test-scripts  - Run script functionality tests"
	@echo "  quality       - Run all quality checks"
	@echo "  lint          - Run linting"
	@echo "  format        - Format code"
	@echo "  clean         - Clean test artifacts"

install:
	pixi install

test:
	pixi run test all

test-fast:
	pixi run test fast

test-integration:
	pixi run test integration

test-slow:
	pixi run test slow

test-generation:
	pixi run test generation

test-scripts:
	pixi run test scripts

quality:
	pixi run quality check

lint:
	pixi run quality lint

format:
	pixi run quality format

clean:
	pixi run clean