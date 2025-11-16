"""Test composition pattern."""

from pathlib import Path


class TestComposition:
    """Test composition pattern."""

    def test_composition(self) -> None:
        """Test composition in parsers."""
        from src.parser.pdf_parser import PDFParser

        pdf = Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf")
        if pdf.exists():
            parser = PDFParser(pdf)
            assert parser is not None
