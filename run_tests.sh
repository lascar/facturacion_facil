#!/bin/bash
# Script to run tests with proper virtual environment activation

echo "🧪 Running tests with virtual environment..."
echo "📁 Working directory: $(pwd)"
echo "🔧 Command: ${*:-all tests}"
echo

# Activate virtual environment directly and run pytest
source ../bin/activate && python -m pytest "$@"
