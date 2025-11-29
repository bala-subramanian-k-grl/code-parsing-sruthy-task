"""
Advanced inheritance & method overriding tests.
"""

from abc import ABC, abstractmethod


class Logger:
    """Simple logger injected via composition."""
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.__instance_id = id(self)
        self.__created = True

    def log(self, msg: str) -> None:
        self.messages.append(msg)

    def __str__(self) -> str:
        return "Logger()"

    def __repr__(self) -> str:
        return "Logger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Logger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Base Class (Abstraction + Encapsulation + Lifecycle)
# ============================================================

class BaseParser(ABC):
    """Abstract base parser demonstrating lifecycle + shared behavior."""

    def __init__(self, logger: Logger | None = None) -> None:
        self.__instance_id = id(self)
        self.__created = True
        self._data: list[str] = []       # Encapsulation
        self._logger = logger or Logger()  # Composition

    def setup(self) -> None:
        self._logger.log("setup")

    @abstractmethod
    def parse(self) -> list[str]:
        """Abstract parse implementation."""

    def teardown(self) -> None:
        self._logger.log("teardown")

    def execute(self) -> list[str]:
        """Run lifecycle: setup → parse → teardown."""
        self.setup()
        result = self.parse()
        self.teardown()
        return result

    def get_data(self) -> list[str]:
        """Shared behavior from base class."""
        return self._data

    def __str__(self) -> str:
        return "BaseParser()"

    def __repr__(self) -> str:
        return "BaseParser()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, BaseParser)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Derived Classes (Inheritance + Polymorphism)
# ============================================================

class TOCParser(BaseParser):
    """TOC parser inheriting from base and overriding parse method."""

    def parse(self) -> list[str]:
        self._data = ["toc1", "toc2"]
        self._logger.log("parsed TOC")
        return self._data

    def __str__(self) -> str:
        return "TOCParser()"

    def __repr__(self) -> str:
        return "TOCParser()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TOCParser)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ContentParser(BaseParser):
    """Content parser inheriting from base and overriding parse method."""

    def parse(self) -> list[str]:
        self._data = ["content1", "content2", "content3"]
        self._logger.log("parsed CONTENT")
        return self._data

    def __str__(self) -> str:
        return "ContentParser()"

    def __repr__(self) -> str:
        return "ContentParser()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ContentParser)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


# ============================================================
# Test Suite
# ============================================================

class TestInheritance:
    """Test inheritance behavior and method overriding."""

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

    def test_inheritance_relationship(self) -> None:
        toc = TOCParser()
        content = ContentParser()

        assert isinstance(toc, BaseParser)
        assert isinstance(content, BaseParser)

    def test_toc_parser_execution(self) -> None:
        logger = Logger()
        parser = TOCParser(logger)
        result = parser.execute()

        assert result == ["toc1", "toc2"]
        assert "parsed TOC" in logger.messages
        assert "setup" in logger.messages
        assert "teardown" in logger.messages

    def test_content_parser_execution(self) -> None:
        logger = Logger()
        parser = ContentParser(logger)
        result = parser.execute()

        assert result == ["content1", "content2", "content3"]
        assert "parsed CONTENT" in logger.messages

    def test_shared_behavior(self) -> None:
        toc = TOCParser()
        content = ContentParser()

        toc.execute()
        content.execute()

        assert toc.get_data() == ["toc1", "toc2"]
        assert content.get_data() == ["content1", "content2", "content3"]

    def test_method_override_polymorphism(self) -> None:
        parsers: list[BaseParser] = [TOCParser(), ContentParser()]
        results = [p.execute() for p in parsers]

        assert results[0] == ["toc1", "toc2"]
        assert results[1] == ["content1", "content2", "content3"]

    def __str__(self) -> str:
        return "TestInheritance()"

    def __repr__(self) -> str:
        return "TestInheritance()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TestInheritance)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
