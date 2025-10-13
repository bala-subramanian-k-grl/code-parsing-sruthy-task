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

    def __init__(self, name: str):
        self._name = name  # Encapsulation
        self._profiler = cProfile.Profile()  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)  # Encapsulation

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
            ps.sort_stats("cumulative").print_stats(5)

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

    def profile_operation(self) -> dict[str, Any]:  # Polymorphism
        """Profile config operations."""
        self._logger.info(f"Profiling {self._name}")
        profile_data = self._run_profiled(self._config_operations)

        return {
            "profiler": self._name,
            "operations": 100,
            "total_calls": profile_data["total_calls"],
            "profile_stats": profile_data["profile_output"][:300] + "...",
        }

    def _config_operations(self) -> int:  # Encapsulation
        """Perform config operations."""
        from src.config import Config

        count = 0
        for _ in range(100):
            config: Config = Config("application.yml")
            _ = config.pdf_input_file
            count += 1
        return count


class ModelProfiler(BaseProfiler):  # Inheritance
    """Model profiler (Inheritance, Polymorphism)."""

    def profile_operation(self) -> dict[str, Any]:  # Polymorphism
        """Profile model operations."""
        self._logger.info(f"Profiling {self._name}")
        profile_data = self._run_profiled(self._model_operations)

        return {
            "profiler": self._name,
            "operations": 200,
            "total_calls": profile_data["total_calls"],
            "profile_stats": profile_data["profile_output"][:300] + "...",
        }

    def _model_operations(self) -> int:  # Encapsulation
        """Perform model operations."""
        from src.core.models import BaseContent, TOCEntry

        count = 0
        for i in range(200):
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
        self._logger = logging.getLogger(self.__class__.__name__)  # Encapsulation

    def add_profiler(self, profiler: BaseProfiler) -> None:  # Polymorphism
        """Add profiler to suite."""
        self._profilers.append(profiler)
        self._logger.info(f"Added profiler: {profiler._name}")

    def run_all(self) -> dict[str, Any]:  # Abstraction
        """Run all profilers."""
        results: dict[str, Any] = {}
        for profiler in self._profilers:
            try:
                result = profiler.profile_operation()  # Polymorphism
                results[result["profiler"]] = result
            except Exception as e:
                self._logger.error(f"Profiler {profiler._name} failed: {e}")
        return results


class ProfilerFactory:  # Factory pattern
    """Profiler factory (Abstraction, Encapsulation)."""

    @staticmethod
    def create_profiler(profiler_type: str, name: str) -> BaseProfiler:
        """Create profiler instance."""
        if profiler_type == "config":
            return ConfigProfiler(name)  # Polymorphism
        elif profiler_type == "model":
            return ModelProfiler(name)  # Polymorphism
        raise ValueError(f"Invalid profiler type: {profiler_type}")


def main():
    """Run performance profiling with OOP principles."""
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    try:
        suite = ProfilerSuite()

        # Add profilers using factory
        suite.add_profiler(ProfilerFactory.create_profiler("config", "Config Profiler"))
        suite.add_profiler(ProfilerFactory.create_profiler("model", "Model Profiler"))

        # Run profiling
        results = suite.run_all()

        logger.info("Performance Profiling Results:")
        for name, result in results.items():
            logger.info(f"Profiler: {name} - {result['operations']} operations")
            logger.info(f"  Total Calls: {result['total_calls']}")

        return 0
    except Exception as e:
        logger.error(f"Profiling failed: {e}")
        return 1


if __name__ == "__main__":
    main()
