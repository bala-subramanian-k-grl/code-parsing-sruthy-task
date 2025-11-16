# Test Suite

Comprehensive test suite for the PDF Parser project, verifying functionality, OOP adherence, and performance.

## Prerequisites
- Python 3.9+
- pytest

## Installation
```bash
pip install -r requirements.txt
```

## Structure
- **common/** - Base test classes, mixins (CleanupMixin, TimerMixin), and test strategies
- **helpers/** - Utilities for file management, mock data generation, validation, and performance testing
- **fixtures/** - Pytest fixtures and mock objects for test setup
- **oop_tests/** - Tests validating OOP principles (encapsulation, inheritance, polymorphism, composition)
- **functional_tests/** - Tests for core features (parsing, validation, extraction)
- **performance_tests/** - Benchmarking and scalability tests
- **coverage_tests/** - Tests to boost code coverage
- **regression_tests/** - Tests to prevent reintroduction of bugs

## Run Tests
```bash
# Run all tests
pytest tests/

# Run specific test category
pytest tests/oop_tests/
pytest tests/functional_tests/

# Run with coverage
pytest tests/ --cov=src
```
