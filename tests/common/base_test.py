"""Enterprise-style Base test class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class BaseTest(ABC):
    """
    Abstract base test class with a standard structure.

    Provides:
    - setup_method()
    - test_basic_functionality()
    - teardown_method()
    - run() executor with safe error capture
    """

    # ------------------------------------------------------------
    # Required abstract methods (polymorphism)
    # ------------------------------------------------------------
    @abstractmethod
    def setup_method(self) -> None:
        """Setup called before each test method."""
        raise NotImplementedError

    @abstractmethod
    def teardown_method(self) -> None:
        """Teardown called after each test method."""
        raise NotImplementedError

    @abstractmethod
    def test_basic_functionality(self) -> None:
        """Main test logic. Must be implemented by subclasses."""
        raise NotImplementedError

    @abstractmethod
    def validate(self) -> bool:
        """Validate test can run."""
        raise NotImplementedError

    @abstractmethod
    def get_name(self) -> str:
        """Get test name."""
        raise NotImplementedError

    # ------------------------------------------------------------
    # Optional hooks (subclasses may override)
    # ------------------------------------------------------------
    def on_test_pass(self) -> None:
        """Hook executed when a test passes."""
        return None

    def on_test_fail(self, error: Exception) -> None:
        """Hook executed when a test fails."""
        return None

    # ------------------------------------------------------------
    # Test Runner
    # ------------------------------------------------------------
    def run(self) -> dict[str, Any]:
        """
        Run the test with:
        - setup
        - execution
        - teardown
        - safe error capture
        """
        test_name = self.__class__.__name__

        try:
            self.setup_method()
            self.test_basic_functionality()
            self.on_test_pass()
            return {"status": "passed", "test": test_name}

        except Exception as e:
            self.on_test_fail(e)
            return {
                "status": "failed",
                "test": test_name,
                "error": str(e),
            }

        finally:
            # teardown is always attempted
            try:
                self.teardown_method()
            except Exception as teardown_err:
                # Teardown errors should not hide the original test error
                print(f"[Teardown Warning] {test_name}: {teardown_err}")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
