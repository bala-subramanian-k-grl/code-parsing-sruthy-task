"""USB PD Specification Parser - Main Entry Point with OOP."""

from abc import ABC, abstractmethod
from typing import Any, Optional

from src.interfaces.app import CLIApp


class BaseRunner(ABC):  # Abstraction
    """Abstract application runner."""

    def __init__(self) -> None:
        self._app: Optional[Any] = None  # Protected attribute

    @abstractmethod
    def create_app(self) -> Any:
        """Create application instance."""
        pass

    def run(self) -> None:
        """Run the application."""
        self._app = self.create_app()
        self._execute()

    def _execute(self) -> None:
        """Execute the application."""
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
        raise ValueError(f"Invalid runner type: {runner_type}")


def main() -> None:
    """Main entry point using OOP principles."""
    # Setup stream logger to capture all output to parser.log
    import logging
    from pathlib import Path

    log_file = Path("outputs") / "parser.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Configure root logger to write to file
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )

    # Factory pattern
    runner = ApplicationFactory.create_runner("cli")
    runner.run()


if __name__ == "__main__":
    main()
