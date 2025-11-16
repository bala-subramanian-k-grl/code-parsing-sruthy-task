"""Test inheritance patterns."""

from abc import ABC, abstractmethod


class BaseParser(ABC):
    """Base parser class."""

    def __init__(self) -> None:
        """Initialize parser."""
        self._data: list[str] = []

    @abstractmethod
    def parse(self) -> list[str]:
        """Parse data."""

    def get_data(self) -> list[str]:
        """Get parsed data."""
        return self._data


class TOCParser(BaseParser):
    """TOC parser inheriting from base."""

    def parse(self) -> list[str]:
        """Parse TOC data."""
        self._data = ["toc1", "toc2"]
        return self._data


class ContentParser(BaseParser):
    """Content parser inheriting from base."""

    def parse(self) -> list[str]:
        """Parse content data."""
        self._data = ["content1", "content2", "content3"]
        return self._data


class TestInheritance:
    """Test inheritance patterns."""

    def test_toc_parser_inheritance(self) -> None:
        """Test TOC parser inherits from base."""
        parser = TOCParser()
        assert isinstance(parser, BaseParser)
        result = parser.parse()
        assert len(result) == 2

    def test_content_parser_inheritance(self) -> None:
        """Test content parser inherits from base."""
        parser = ContentParser()
        assert isinstance(parser, BaseParser)
        result = parser.parse()
        assert len(result) == 3

    def test_shared_behavior(self) -> None:
        """Test shared behavior from base class."""
        toc = TOCParser()
        content = ContentParser()

        toc.parse()
        content.parse()

        assert toc.get_data() == ["toc1", "toc2"]
        assert content.get_data() == [
            "content1",
            "content2",
            "content3",
        ]

    def test_method_override(self) -> None:
        """Test method overriding."""
        parsers: list[BaseParser] = [TOCParser(), ContentParser()]
        results = [p.parse() for p in parsers]

        assert len(results[0]) == 2
        assert len(results[1]) == 3
