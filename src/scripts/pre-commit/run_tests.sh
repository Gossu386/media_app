#!/bin/bash
set -e  # Exit on error

echo "Running pytest..."

# Use python -m to run pytest, which works with any environment (venv, system, etc.)
python -m pytest src/tests

echo "✓ All tests passed"