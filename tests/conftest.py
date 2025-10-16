"""Minimal test configuration with OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path

import pytest


class BaseFixture(ABC):  # Abstraction
    def __init__(self) -> None:
        self._data = {}  # Encapsulation

    @abstractmethod  # Abstraction
    def create(self, tmp_path: Path) -> Path:
        pass


class ConfigFixture(BaseFixture):  # Inheritance
    def create(self, tmp_path: Path) -> Path:  # Polymorphism
        config_file = tmp_path / "test.yml"
        config_content = "pdf_input_file: test.pdf\noutput_directory: outputs"
        config_file.write_text(config_content)
        return config_file


class PDFFixture(BaseFixture):  # Inheritance
    def create(self, tmp_path: Path) -> Path:  # Polymorphism
        pdf_file = tmp_path / "test.pdf"
        pdf_file.write_text("Mock PDF")
        return pdf_file


class FixtureFactory:  # Encapsulation
    def __init__(self) -> None:
        self._fixtures: dict[str, BaseFixture] = {}  # Encapsulation

    def register(
        self, name: str, fixture: BaseFixture
    ) -> None:  # Polymorphism
        self._fixtures[name] = fixture

    def create(self, name: str, tmp_path: Path) -> Path:  # Abstraction
        return self._fixtures[name].create(tmp_path)


@pytest.fixture
def fixture_factory():
    factory = FixtureFactory()
    factory.register("config", ConfigFixture())
    factory.register("pdf", PDFFixture())
    return factory
