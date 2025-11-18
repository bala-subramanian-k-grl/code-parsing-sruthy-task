"""Comprehensive test package for PDF Parser project.

This package contains various types of tests:
- common: Base classes, mixins, and test strategies
- fixtures: Pytest fixtures and mock objects
- helpers: Utility functions for testing
- oop_tests: Tests validating OOP principles
- functional_tests: Tests for core features
- performance_tests: Benchmarking and scalability tests
- coverage_tests: Tests to boost code coverage
- regression_tests: Tests to prevent bug reintroduction
"""

from . import (common, coverage_tests, fixtures, functional_tests, helpers,
               oop_tests, performance_tests, regression_tests)

__all__ = [
    "common",
    "fixtures",
    "helpers",
    "oop_tests",
    "functional_tests",
    "performance_tests",
    "coverage_tests",
    "regression_tests",
]
