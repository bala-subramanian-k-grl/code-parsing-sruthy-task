#!/usr/bin/env python3
# USB PD Specification Parser - Performance Profiler
"""Performance profiler with OOP principles."""

import cProfile
import logging
import pstats
from abc import ABC, abstractmethod
from io import StringIO
from typing import Any, Callable


class BaseProfiler(ABC):  # Abstraction
    """Abstract profiler (Abstraction, Encapsulation)."""

    def __init__(self, name: str, stats_count: int = 5):
        self._name = name  # Encapsulation
        self._stats_count = stats_count  # Encapsulation
        self._profiler = cProfile.Profile()  # Encapsulation
        class_name = self.__class__.__name__
        self._logger = logging.getLogger(class_name)

    @property
    def name(self) -> str:
        """Get profiler name."""
        return self._name

    @abstractmethod  # Abstraction
    def profile_operation(self) -> dict[str, Any]:
        pass

    def _run_profiled(
        self, func: Callable[..., Any], *args: Any
    ) -> dict[str, Any]:  # Encapsulation
        """Run function with profiling."""
        try:
            self._profiler.enable()
            result: Any = func(*args)
            self._profiler.disable()

            s = StringIO()
            ps = pstats.Stats(self._profiler, stream=s)
            ps.sort_stats("cumulative").print_stats(self._stats_count)

            return {
                "result": result,
                "profile_output": s.getvalue(),
                "total_calls": getattr(ps, "total_calls", 0),
            }
        except Exception as e:
            self._logger.error(f"Profiling failed: {e}")
            raise


class ConfigProfiler(BaseProfiler):  # Inheritance
    """Config profiler (Inheritance, Polymorphism)."""

    def __init__(self, name: str, operations: int = 100, stats_count: int = 5):
        super().__init__(name, stats_count)
        self._operations = operations

    def profile_operation(self) -> dict[str, Any]:  # Polymorphism
        """Profile config operations."""
        self._logger.info(f"Profiling {self._name}")
        profile_data = self._run_profiled(self._config_operations)

        return {
            "profiler": self._name,
            "operations": self._operations,
            "total_calls": profile_data["total_calls"],
            "profile_stats": (profile_data["profile_output"][:300] + "..."),
        }

    def _config_operations(self) -> int:  # Encapsulation
        """Perform config operations."""
        from src.config import Config

        count = 0
        for _ in range(self._operations):
            config: Config = Config("application.yml")
            _ = config.pdf_input_file
            count += 1
        return count


class ModelProfiler(BaseProfiler):  # Inheritance
    """Model profiler (Inheritance, Polymorphism)."""

    def __init__(self, name: str, operations: int = 200, stats_count: int = 5):
        super().__init__(name, stats_count)
        self._operations = operations

    def profile_operation(self) -> dict[str, Any]:  # Polymorphism
        """Profile model operations."""
        self._logger.info(f"Profiling {self._name}")
        profile_data = self._run_profiled(self._model_operations)

        return {
            "profiler": self._name,
            "operations": self._operations,
            "total_calls": profile_data["total_calls"],
            "profile_stats": (profile_data["profile_output"][:300] + "..."),
        }

    def _model_operations(self) -> int:  # Encapsulation
        """Perform model operations."""
        from src.core.models import BaseContent, TOCEntry

        count = 0
        for i in range(self._operations):
            BaseContent(page=i + 1, content=f"test {i}")
            if i % 20 == 0:
                TOCEntry(
                    doc_title="Profile",
                    section_id=f"S{i}",
                    title=f"Title {i}",
                    full_path=f"Path {i}",
                    page=i + 1,
                    level=1,
                )
            count += 1
        return count


class ProfilerSuite:  # Encapsulation
    """Profiler suite (Encapsulation, Abstraction)."""

    def __init__(self):
        self._profilers: list[BaseProfiler] = []  # Encapsulation
        class_name = self.__class__.__name__
        self._logger = logging.getLogger(class_name)

    def add_profiler(self, profiler: BaseProfiler) -> None:  # Polymorphism
        """Add profiler to suite."""
        self._profilers.append(profiler)
        self._logger.info(f"Added profiler: {profiler.name}")

    def run_all(self) -> dict[str, Any]:  # Abstraction
        """Run all profilers."""
        results: dict[str, Any] = {}
        for profiler in self._profilers:
            try:
                result = profiler.profile_operation()  # Polymorphism
                results[result["profiler"]] = result
            except Exception as e:
                msg = f"Profiler {profiler.name} failed: {e}"
                self._logger.error(msg)
        return results


class ProfilerFactory:  # Factory pattern
    """Profiler factory (Abstraction, Encapsulation)."""

    @staticmethod
    def create_profiler(
        profiler_type: str, name: str, operations: int | None = None
    ) -> BaseProfiler:
        """Create profiler instance."""
        if profiler_type == "config":
            return ConfigProfiler(name, operations or 100)  # Polymorphism
        elif profiler_type == "model":
            return ModelProfiler(name, operations or 200)  # Polymorphism
        msg = f"Invalid profiler type: {profiler_type}. Supported types: config, model"
        raise ValueError(msg)


def main():
    """Run performance profiling with OOP principles."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        suite = ProfilerSuite()

        # Add profilers using factory
        config_profiler = ProfilerFactory.create_profiler(
            "config", "Config Profiler"
        )
        suite.add_profiler(config_profiler)
        model_profiler = ProfilerFactory.create_profiler(
            "model", "Model Profiler"
        )
        suite.add_profiler(model_profiler)

        # Run profiling
        results = suite.run_all()

        logger.info("Performance Profiling Results:")
        for name, result in results.items():
            ops = result["operations"]
            logger.info(f"Profiler: {name} - {ops} operations")
            calls = result["total_calls"]
            logger.info(f"  Total Calls: {calls}")

        return 0
    except Exception as e:
        logger.error(f"Profiling failed: {e}")
        return 1


if __name__ == "__main__":
    main()
