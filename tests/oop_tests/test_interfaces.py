"""Test interface-based design."""

from typing import Protocol


class ReaderProtocol(Protocol):
    """Reader interface protocol."""

    def read(self) -> str:
        """Read data."""


class WriterProtocol(Protocol):
    """Writer interface protocol."""

    def write(self, data: str) -> None:
        """Write data."""


class FileReader:
    """File reader implementation."""

    def read(self) -> str:
        """Read from file."""
        return "file_data"


class MemoryReader:
    """Memory reader implementation."""

    def read(self) -> str:
        """Read from memory."""
        return "memory_data"


class FileWriter:
    """File writer implementation."""

    def write(self, data: str) -> None:
        """Write to file."""
        self.data = data


def process_reader(reader: ReaderProtocol) -> str:
    """Process any reader implementation."""
    return reader.read()


class TestInterfaces:
    """Test interface-based design."""

    def test_file_reader_interface(self) -> None:
        """Test file reader implements interface."""
        reader = FileReader()
        result = process_reader(reader)
        assert result == "file_data"

    def test_memory_reader_interface(self) -> None:
        """Test memory reader implements interface."""
        reader = MemoryReader()
        result = process_reader(reader)
        assert result == "memory_data"

    def test_writer_interface(self) -> None:
        """Test writer interface."""
        writer: WriterProtocol = FileWriter()
        writer.write("test")
        assert writer.data == "test"
