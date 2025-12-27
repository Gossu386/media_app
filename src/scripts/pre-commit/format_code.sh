#!/bin/bash
set -e  # Exit on error

echo "Running Ruff code formatting..."

# Use python -m to run ruff, which works with any environment (venv, system, etc.)
python -m ruff check src --fix
python -m ruff format src

echo "✓ Ruff formatting completed successfully"

