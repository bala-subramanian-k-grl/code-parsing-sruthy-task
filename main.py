"""USB PD Specification Parser - Main Entry Point with Enhanced OOP."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from src.cli.app import CLIApp
from src.utils.logger import logger
from src.utils.timer import timer


# ===============================================================
# 1. Base Runner (Abstraction + Template Pattern)
# ===============================================================
class BaseRunner(ABC):
    """Abstract application runner with lifecycle hooks."""

    def __init__(self) -> None:
        self._app: Optional[CLIApp] = None  # Protected attribute

    # ---------- Polymorphic Factory Method ----------
    @abstractmethod
    def create_app(self) -> CLIApp:
        """Create and return a CLI application instance."""

    # ---------- Template Method ----------
    def run(self) -> None:
        """Run the application using lifecycle hooks."""
        self._before_run()
        self._app = self.create_app()
        self._execute()
        self._after_run()

    # ---------- Lifecycle Hooks ----------
    def _before_run(self) -> None:
        logger.info("Application runner initializing...")

    def _after_run(self) -> None:
        logger.info("Application runner completed.")

    def _execute(self) -> None:
        """Execute the created application."""
        if self._app:
            self._app.run()


# ===============================================================
# 2. CLI Runner (Inheritance + Polymorphism)
# ===============================================================
class CLIRunner(BaseRunner):
    """Runner for console / terminal mode."""

    def create_app(self) -> CLIApp:
        return CLIApp()


# ===============================================================
# 3. Application Factory (Factory Pattern + Overloading)
# ===============================================================
class ApplicationFactory:
    """Factory for creating application runners."""

    @staticmethod
    def create_runner(runner_type: str = "cli") -> BaseRunner:
        """Create a runner based on type."""
        runner_lower = runner_type.lower()
        if runner_lower == "cli":
            return CLIRunner()
        raise ValueError(
            f"Invalid runner type: {runner_type}. Supported: cli"
        )


# ===============================================================
# 4. Main Entry Point (Timer + Logging)
# ===============================================================
@timer
def main() -> None:
    """Main entry point using OOP principles."""
    logger.info("USB PD Specification Parser started.")

    runner = ApplicationFactory.create_runner("cli")
    runner.run()

    logger.info("USB PD Specification Parser finished successfully.")


# ===============================================================
# 5. Run Only If Script
# ===============================================================
if __name__ == "__main__":
    main()
