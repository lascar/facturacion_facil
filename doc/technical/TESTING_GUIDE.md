# Testing Guide

This guide explains how to run tests in the Facturación Fácil project.

## Prerequisites

Make sure you have the virtual environment set up and all dependencies installed:

```bash
# Activate the virtual environment
source ../bin/activate

# Install dependencies (if not already done)
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

## Running Tests

### Method 1: Using the Test Scripts (Recommended)

We provide two convenient scripts that automatically activate the virtual environment:

#### Bash Script (Linux/Mac)
```bash
# Run all tests
./run_tests.sh

# Run specific test files
./run_tests.sh tests/test_advanced/test_property_based.py

# Run with specific pytest options
./run_tests.sh tests/ -v --tb=short

# Run a specific test
./run_tests.sh tests/test_advanced/test_property_based.py::TestPropertyBased::test_precio_always_positive -v
```

#### Python Script (Cross-platform)
```bash
# Run all tests
python3 run_tests_fixed.py

# Run specific test files
python3 run_tests_fixed.py tests/test_advanced/test_property_based.py

# Run with specific pytest options
python3 run_tests_fixed.py tests/ -v --tb=short
```

### Method 2: Manual Virtual Environment Activation

```bash
# Activate virtual environment and run tests
source ../bin/activate && python -m pytest

# Run specific tests
source ../bin/activate && python -m pytest tests/test_advanced/test_property_based.py -v
```

## Test Categories

The project includes several types of tests:

### 1. Unit Tests
- **Location**: `tests/test_database/`, `tests/test_utils/`
- **Purpose**: Test individual components and functions
- **Example**: `./run_tests.sh tests/test_database/test_models.py`

### 2. UI Tests
- **Location**: `tests/test_ui/`, `tests/test_facturas/`
- **Purpose**: Test user interface components
- **Example**: `./run_tests.sh tests/test_ui/test_productos.py`

### 3. Integration Tests
- **Location**: `tests/test_advanced/test_integration.py`
- **Purpose**: Test component interactions
- **Example**: `./run_tests.sh tests/test_advanced/test_integration.py`

### 4. Property-Based Tests
- **Location**: `tests/test_advanced/test_property_based.py`
- **Purpose**: Test properties using Hypothesis
- **Example**: `./run_tests.sh tests/test_advanced/test_property_based.py`

### 5. Regression Tests
- **Location**: `tests/test_regression/`
- **Purpose**: Prevent bugs from reappearing
- **Example**: `./run_tests.sh tests/test_regression/`

### 6. Performance Tests
- **Location**: `tests/test_advanced/test_performance.py`
- **Purpose**: Benchmark and performance testing
- **Example**: `./run_tests.sh tests/test_advanced/test_performance.py`

## Common Test Commands

```bash
# Run all tests with coverage
./run_tests.sh --cov=. --cov-report=html

# Run tests in parallel (faster)
./run_tests.sh -n auto

# Run only failed tests from last run
./run_tests.sh --lf

# Run tests with verbose output
./run_tests.sh -v

# Run tests and stop on first failure
./run_tests.sh -x

# Run tests matching a pattern
./run_tests.sh -k "test_producto"

# Run tests with specific markers
./run_tests.sh -m "unit"
./run_tests.sh -m "integration"
./run_tests.sh -m "ui"
```

## Test Markers

The project uses pytest markers to categorize tests:

- `@pytest.mark.unit`: Unit tests
- `@pytest.mark.integration`: Integration tests
- `@pytest.mark.ui`: UI tests
- `@pytest.mark.slow`: Slow running tests
- `@pytest.mark.performance`: Performance tests
- `@pytest.mark.regression`: Regression tests

## Troubleshooting

### Import Errors
If you see `ModuleNotFoundError` for packages like `hypothesis` or `customtkinter`:

1. Make sure you're using the test scripts: `./run_tests.sh` or `python3 run_tests_fixed.py`
2. Or manually activate the virtual environment: `source activate_env.sh`
3. Check that dependencies are installed: `pip list | grep -E "(hypothesis|customtkinter|pytest)"`

### Virtual Environment Issues
If the virtual environment isn't working:

1. Check that `activate_env.sh` exists and is executable
2. Make sure the virtual environment is in the correct location (`../bin/activate`)
3. Reinstall dependencies if needed

### Test Failures
If tests are failing:

1. Run with verbose output: `./run_tests.sh -v`
2. Run a single failing test to isolate the issue
3. Check the test logs and error messages
4. Ensure the database is in a clean state

## Coverage Reports

After running tests with coverage, you can view the HTML report:

```bash
# Generate coverage report
./run_tests.sh --cov=. --cov-report=html

# Open the report (Linux)
xdg-open htmlcov/index.html

# Open the report (Mac)
open htmlcov/index.html
```

## Continuous Integration

The test suite is designed to run in CI environments. All 336 tests should pass for a successful build.

Current test statistics:
- **Total tests**: 336
- **Test categories**: Unit, Integration, UI, Property-based, Regression, Performance
- **Coverage**: ~26% (improving with each test run)
- **All previously failing tests**: ✅ Fixed and passing
