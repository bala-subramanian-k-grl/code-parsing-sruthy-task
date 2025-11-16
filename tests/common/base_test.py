"""Base test class."""

from abc import ABC, abstractmethod
from typing import Any


class BaseTest(ABC):
    """Abstract base test class with common test structure.
    
    Provides a template for test classes with setup/teardown
    and required test methods.
    """

    def setup_method(self) -> None:
        """Setup method called before each test method."""
        pass

    def teardown_method(self) -> None:
        """Teardown method called after each test method."""
        pass

    @abstractmethod
    def test_basic_functionality(self) -> None:
        """Test basic functionality - must be implemented by subclasses."""

    def run(self) -> dict[str, Any]:
        """Run the test and return results."""
        try:
            self.setup_method()
            self.test_basic_functionality()
            return {"status": "passed", "test": self.__class__.__name__}
        except Exception as e:
            return {
                "status": "failed",
                "test": self.__class__.__name__,
                "error": str(e),
            }
        finally:
            self.teardown_method()
