"""
PDF to Markdown conversion service using PyMuPDF (fitz).
Extracts text and structure from PDF files and formats as Markdown.
"""

import asyncio
from pathlib import Path

import fitz  # PyMuPDF

from app.services.converter import ConversionError

# Font-size thresholds for Markdown heading detection.
# Lines whose largest span meets or exceeds a threshold are promoted to
# the corresponding heading level.
_H1_SIZE = 20
_H2_SIZE = 16
_H3_SIZE = 14
_H3_BOLD_SIZE = 12  # body-sized bold text that still warrants an H3


class PdfConvertService:
    """Converts PDF files to Markdown using PyMuPDF."""

    def can_convert(self, input_format: str, output_format: str) -> bool:
        """Return True only for PDF→Markdown conversions."""
        return input_format.lower() == "pdf" and output_format.lower() == "md"

    async def convert_to_markdown(
        self,
        input_file_path: Path,
        output_file_path: Path,
    ) -> Path:
        """
        Convert a PDF file to Markdown, running the blocking I/O in a
        thread so we don't stall the event loop.

        Args:
            input_file_path: Path to the source PDF.
            output_file_path: Where to write the resulting Markdown file.

        Returns:
            Path to the converted Markdown file.

        Raises:
            ConversionError: If conversion fails.
        """
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._convert_sync,
            input_file_path,
            output_file_path,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_sync(input_path: Path, output_path: Path) -> Path:
        """Synchronous PDF→Markdown conversion executed in a thread."""
        try:
            doc = fitz.open(str(input_path))
            markdown_parts: list[str] = []

            for page_num, page in enumerate(doc, start=1):
                if page_num > 1:
                    markdown_parts.append("\n\n---\n\n")

                blocks = page.get_text(
                    "dict",
                    # TEXT_PRESERVE_LIGATURES keeps ligature characters
                    # (e.g. "fi", "fl") as single glyphs so they round-trip
                    # correctly rather than being split into two characters.
                    flags=fitz.TEXT_PRESERVE_LIGATURES,
                )["blocks"]

                for block in blocks:
                    if block.get("type") != 0:  # 0 = text block
                        continue

                    block_lines: list[str] = []
                    for line in block.get("lines", []):
                        spans = line.get("spans", [])
                        if not spans:
                            continue

                        text = "".join(s["text"] for s in spans).strip()
                        if not text:
                            continue

                        # Determine heading level by the largest font size in the line
                        max_size = max(s["size"] for s in spans)
                        is_bold = any(
                            "bold" in s.get("font", "").lower() for s in spans
                        )

                        if max_size >= _H1_SIZE or (max_size >= _H2_SIZE and is_bold):
                            text = f"# {text}"
                        elif max_size >= _H2_SIZE or (max_size >= _H3_SIZE and is_bold):
                            text = f"## {text}"
                        elif max_size >= _H3_SIZE or (max_size >= _H3_BOLD_SIZE and is_bold):
                            text = f"### {text}"

                        block_lines.append(text)

                    if block_lines:
                        markdown_parts.append("\n".join(block_lines))

            doc.close()

            markdown_text = "\n\n".join(markdown_parts)
            output_path.write_text(markdown_text, encoding="utf-8")
            return output_path

        except Exception as e:
            raise ConversionError(f"PDF to Markdown conversion failed: {e}") from e


# Singleton
pdf_convert_service = PdfConvertService()
