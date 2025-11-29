"""Test composition pattern with dependency injection."""


class DummyLogger:
    """Simple logger for testing composition."""
    def __init__(self) -> None:
        self.messages: list[str] = []
        self.__instance_id = id(self)
        self.__created = True

    def log(self, msg: str) -> None:
        self.messages.append(msg)

    def __str__(self) -> str:
        return "DummyLogger()"

    def __repr__(self) -> str:
        return "DummyLogger()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DummyLogger)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class DummyEngine:
    """A dummy dependency used to demonstrate composition."""
    def __init__(self, logger: DummyLogger) -> None:
        self.logger = logger
        self.__instance_id = id(self)
        self.__created = True

    def process(self) -> str:
        self.logger.log("Engine processed")
        return "ok"

    def __str__(self) -> str:
        return "DummyEngine()"

    def __repr__(self) -> str:
        return "DummyEngine()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, DummyEngine)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class ComposedObject:
    """Object using composition by accepting dependencies via constructor."""
    def __init__(self, engine: DummyEngine) -> None:
        self.engine = engine
        self.__instance_id = id(self)
        self.__created = True

    def run(self) -> str:
        return self.engine.process()

    def __str__(self) -> str:
        return "ComposedObject()"

    def __repr__(self) -> str:
        return "ComposedObject()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ComposedObject)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True


class TestComposition:
    """Test composition pattern."""

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

    def test_composition_with_injected_dependency(self) -> None:
        logger = DummyLogger()
        engine = DummyEngine(logger)
        obj = ComposedObject(engine)

        assert obj.run() == "ok"
        assert "Engine processed" in logger.messages

    def __str__(self) -> str:
        return "TestComposition()"

    def __repr__(self) -> str:
        return "TestComposition()"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, TestComposition)

    def __hash__(self) -> int:
        return hash(self.__class__.__name__)

    def __bool__(self) -> bool:
        return True
