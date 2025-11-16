"""USB PD Specification Parser - Main Entry Point with OOP."""

from abc import ABC, abstractmethod
from typing import Optional

from src.cli.app import CLIApp
from src.utils.logger import logger
from src.utils.timer import timer


class BaseRunner(ABC):  # Abstraction
    """Abstract application runner."""

    def __init__(self) -> None:
        self._app: Optional[CLIApp] = None  # Protected attribute

    @abstractmethod
    def create_app(self) -> CLIApp:
        """Create application instance."""

    def run(self) -> None:
        """Run the application."""
        self._app = self.create_app()
        self._execute()

    def _execute(self) -> None:
        """Execute the application by calling its run method."""
        if self._app:
            self._app.run()


class CLIRunner(BaseRunner):  # Inheritance
    """CLI application runner."""

    def create_app(self) -> CLIApp:
        """Create CLI application instance."""
        return CLIApp()


class ApplicationFactory:
    """Application factory."""

    @staticmethod
    def create_runner(runner_type: str = "cli") -> BaseRunner:
        """Create runner instance."""
        if runner_type == "cli":
            return CLIRunner()
        raise ValueError(f"Invalid runner type: {runner_type}. Supported types: cli")


@timer
def main() -> None:
    """Main entry point using OOP principles."""
    logger.info("USB PD Specification Parser started")

    runner = ApplicationFactory.create_runner("cli")
    runner.run()

    logger.info("USB PD Specification Parser completed")


if __name__ == "__main__":
    main()
