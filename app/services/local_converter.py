"""
Local image conversion service using Pillow.
Handles common image-to-image conversions without external API calls.
Falls back to CloudConvert for unsupported operations.
"""

import asyncio
from pathlib import Path
from typing import Optional

from PIL import Image

from app.services.converter import ConversionError

# Mapping from format names to Pillow save format strings
_PILLOW_FORMAT_MAP = {
    "jpg": "JPEG",
    "jpeg": "JPEG",
    "png": "PNG",
    "webp": "WEBP",
    "gif": "GIF",
    "ico": "ICO",
}

# Formats that support a quality parameter
_QUALITY_FORMATS = {"JPEG", "WEBP"}


class LocalConvertService:
    """Converts images locally using Pillow."""

    def can_convert(self, output_format: str) -> bool:
        """Check whether Pillow can handle the requested output format."""
        return output_format.lower() in _PILLOW_FORMAT_MAP

    async def convert_image(
        self,
        input_file_path: Path,
        output_format: str,
        output_file_path: Path,
        quality: Optional[int] = None,
        resize_width: Optional[int] = None,
        resize_height: Optional[int] = None,
    ) -> Path:
        """
        Convert an image using Pillow, running the blocking I/O in a
        thread so we don't stall the event loop.

        Args:
            input_file_path: Path to the source image.
            output_format: Target format (jpeg, png, webp, gif).
            output_file_path: Where to write the result.
            quality: Optional quality 1-100 (JPEG / WebP only).
            resize_width: Optional target width in pixels.
            resize_height: Optional target height in pixels.

        Returns:
            Path to the converted file.

        Raises:
            ConversionError: If the local conversion fails.
        """
        pillow_fmt = _PILLOW_FORMAT_MAP.get(output_format.lower())
        if pillow_fmt is None:
            raise ConversionError(
                f"Local conversion does not support '{output_format}'"
            )

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(
            None,
            self._convert_sync,
            input_file_path,
            output_file_path,
            pillow_fmt,
            quality,
            resize_width,
            resize_height,
        )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _convert_sync(
        input_path: Path,
        output_path: Path,
        pillow_fmt: str,
        quality: Optional[int],
        resize_width: Optional[int],
        resize_height: Optional[int],
    ) -> Path:
        """Synchronous conversion logic executed in a thread."""
        try:
            img = Image.open(input_path)

            # Resize if requested
            if resize_width or resize_height:
                img = _resize(img, resize_width, resize_height)

            # Handle transparency: convert RGBA -> RGB for formats that
            # don't support an alpha channel (JPEG).
            if pillow_fmt == "JPEG" and img.mode in ("RGBA", "P", "LA"):
                background = Image.new("RGB", img.size, (255, 255, 255))
                if img.mode == "P":
                    img = img.convert("RGBA")
                background.paste(img, mask=img.split()[-1])
                img = background
            elif pillow_fmt == "JPEG" and img.mode != "RGB":
                img = img.convert("RGB")

            # Build save kwargs
            save_kwargs: dict = {"format": pillow_fmt}

            if pillow_fmt in _QUALITY_FORMATS and quality is not None:
                save_kwargs["quality"] = quality

            # PNG optimisation: always use compression
            if pillow_fmt == "PNG":
                save_kwargs["optimize"] = True

            # GIF: preserve animation frames if present
            if pillow_fmt == "GIF":
                save_kwargs["save_all"] = True

            img.save(output_path, **save_kwargs)
            return output_path

        except Exception as e:
            raise ConversionError(f"Local conversion failed: {e}") from e


def _resize(
    img: Image.Image,
    width: Optional[int],
    height: Optional[int],
) -> Image.Image:
    """Resize an image, preserving aspect ratio when only one dimension is given."""
    orig_w, orig_h = img.size

    if width and height:
        new_size = (width, height)
    elif width:
        ratio = width / orig_w
        new_size = (width, round(orig_h * ratio))
    elif height:
        ratio = height / orig_h
        new_size = (round(orig_w * ratio), height)
    else:
        return img

    return img.resize(new_size, Image.LANCZOS)


# Singleton
local_convert_service = LocalConvertService()
