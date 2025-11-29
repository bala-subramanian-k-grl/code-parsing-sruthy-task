"""Advanced interface/Protocol-based OOP tests with dependency injection."""

from __future__ import annotations

from typing import Protocol, runtime_checkable

# ============================================================
# Protocol Interfaces (Abstraction)
# ============================================================

@runtime_checkable
class ReaderProtocol(Protocol):
    """Reader interface protocol specifying read operation."""
    def read(self) -> str:
        ...


@runtime_checkable
class WriterProtocol(Protocol):
    """Writer interface protocol specifying write operation."""
    def write(self, data: str) -> None:
        ...


# ============================================================
# Implementations (Polymorphism + Encapsulation)
# ============================================================

class FileReader:
    """File reader implementation."""

    def read(self) -> str:
        return "file_data"

    def __str__(self) -> str:
        return "FileReader()"

    def __repr__(self) -> str:
        return "FileReader()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FileReader)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class MemoryReader:
    """Memory reader implementation."""

    def read(self) -> str:
        return "memory_data"

    def __str__(self) -> str:
        return "MemoryReader()"

    def __repr__(self) -> str:
        return "MemoryReader()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, MemoryReader)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class FileWriter:
    """File writer implementation with minimal encapsulation."""

    def __init__(self) -> None:
        self._storage: str | None = None  # Encapsulated

    def write(self, data: str) -> None:
        self._storage = data

    @property
    def data(self) -> str | None:
        return self._storage

    def __str__(self) -> str:
        return "FileWriter()"

    def __repr__(self) -> str:
        return "FileWriter()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, FileWriter)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Composition + Strategy-like usage
# ============================================================

def process_reader(reader: ReaderProtocol) -> str:
    """Process any object implementing ReaderProtocol."""
    return reader.read()


def write_and_return(writer: WriterProtocol, msg: str) -> str:
    """Write via writer and return stored value if available."""
    writer.write(msg)
    return getattr(writer, "data", msg)  # Safe access


# ============================================================
# Test Suite
# ============================================================

class TestInterfaces:
    """Test interface-based design with polymorphism."""

    def __init__(self) -> None:
        self.__test_count = 0
        self.__pass_count = 0
        self.__fail_count = 0

    @property
    def test_count(self) -> int:
        return self.__test_count

    @property
    def pass_count(self) -> int:
        return self.__pass_count

    @property
    def fail_count(self) -> int:
        return self.__fail_count

    def test_file_reader_implements_protocol(self) -> None:
        reader = FileReader()
        result = process_reader(reader)
        assert result == "file_data"

    def test_memory_reader_implements_protocol(self) -> None:
        reader = MemoryReader()
        result = process_reader(reader)
        assert result == "memory_data"

    def test_writer_protocol(self) -> None:
        writer: WriterProtocol = FileWriter()
        output = write_and_return(writer, "hello")

        # Writer should encapsulate written data
        assert writer.data == "hello"
        assert output == "hello"

    def test_polymorphism_with_protocols(self) -> None:
        """Ensure any class satisfying Protocol works."""
        class CustomReader:
            def read(self) -> str:
                return "custom"

            def __str__(self) -> str:
                return "CustomReader()"

            def __repr__(self) -> str:
                return "CustomReader()"

            def __eq__(self, other: object) -> bool:
                return isinstance(other, CustomReader)

            def __hash__(self) -> int:
                return hash(self.__class__.__name__)

            def __bool__(self) -> bool:
                return True

        result = process_reader(CustomReader())
        assert result == "custom"

    def __str__(self) -> str:
        return "TestInterfaces()"

    def __repr__(self) -> str:
        return "TestInterfaces()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TestInterfaces)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
