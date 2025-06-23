"""Image processing utilities: resize, compress while optionally preserving EXIF metadata.

This module exposes three public helpers:
    - resize_image
    - compress_image
    - process_image

Key features
------------
* Pillow ≥ 10 compatible (uses ``Image.Resampling.LANCZOS``).
* Accepts either ``str`` or ``pathlib.Path`` for input paths.
* Produces **unique** output filenames (no silent overwrite).
* Supports most common raster formats (see ``SUPPORTED_INPUT_FORMATS``).
* Optional EXIF preservation via the ``keep_exif`` flag (default: ``True``).
* Always returns ``pathlib.Path`` objects so the caller can chain operations easily.
"""
from __future__ import annotations

import os
from pathlib import Path
from typing import Tuple, Optional

from PIL import Image, UnidentifiedImageError

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

SUPPORTED_INPUT_FORMATS: set[str] = {"JPEG", "PNG", "WEBP", "BMP", "TIFF"}

# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------

def _unique_path(base: Path, suffix: str) -> Path:
    """Return a *unique* output path by appending ``suffix`` (and a counter if
    necessary) before the extension.

    Parameters
    ----------
    base : pathlib.Path
        Base path without extension.
    suffix : str
        Suffix to append (e.g. "_resized" or "_compressed"). Must include the
        leading underscore if desired.
    """
    candidate: Path = base.with_name(f"{base.name}{suffix}.jpg")
    counter = 1
    while candidate.exists():
        candidate = base.with_name(f"{base.name}{suffix}_{counter}.jpg")
        counter += 1
    return candidate


def _convert_if_needed(img: Image.Image) -> Image.Image:
    """Convert paletted / alpha images to RGB to ensure JPEG compatibility."""
    if img.mode in ("P", "RGBA", "LA"):
        return img.convert("RGB")
    return img


# ---------------------------------------------------------------------------
# Public functions
# ---------------------------------------------------------------------------

def resize_image(
    path: str | Path,
    size: Tuple[int, int] = (400, 400),
    *,
    keep_exif: bool = True,
) -> Optional[Path]:
    """Resize *path* to *size* (width, height) and save as JPEG.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to the source image.
    size : (int, int), optional, default (400, 400)
        Target size in pixels.
    keep_exif : bool, optional, default ``True``
        If ``True`` and the source contains EXIF metadata, it will be preserved
        in the output file.

    Returns
    -------
    pathlib.Path | None
        Path of the resized JPEG, or ``None`` if an error occurred.
    """
    p: Path = Path(path)
    try:
        with Image.open(p) as img:
            if img.format not in SUPPORTED_INPUT_FORMATS:
                raise ValueError(f"Format {img.format} non pris en charge.")

            resized = img.resize(size, Image.Resampling.LANCZOS)
            resized = _convert_if_needed(resized)

            base = p.with_suffix("")  # drop extension
            out_path = _unique_path(base, "_resized")

            save_kwargs = {}
            if keep_exif and "exif" in img.info:
                save_kwargs["exif"] = img.info["exif"]

            resized.save(out_path, format="JPEG", **save_kwargs)
            return out_path
    except (FileNotFoundError, UnidentifiedImageError) as exc:
        print(f"Erreur d'ouverture : {exc}")
    except Exception as exc:
        print(f"Erreur inattendue dans resize_image : {exc}")
    return None


def compress_image(
    path: str | Path,
    quality: int = 75,
    *,
    keep_exif: bool = True,
) -> Optional[Path]:
    """Compress *path* to JPEG at the specified *quality*.

    The image is converted to RGB if necessary. If *keep_exif* is ``True`` and
    EXIF bytes are present, they are copied to the output.
    """
    p: Path = Path(path)
    try:
        with Image.open(p) as img:
            if img.format not in SUPPORTED_INPUT_FORMATS:
                raise ValueError(f"Format {img.format} non pris en charge.")

            img = _convert_if_needed(img)
            base = p.with_suffix("")
            out_path = _unique_path(base, "_compressed")

            save_kwargs = {"quality": quality, "optimize": True}
            if keep_exif and "exif" in img.info:
                save_kwargs["exif"] = img.info["exif"]

            img.save(out_path, format="JPEG", **save_kwargs)
            return out_path
    except (FileNotFoundError, UnidentifiedImageError) as exc:
        print(f"Erreur d'ouverture : {exc}")
    except Exception as exc:
        print(f"Erreur inattendue dans compress_image : {exc}")
    return None


def process_image(
    path: str | Path,
    size: Tuple[int, int] = (400, 400),
    quality: int = 75,
    *,
    keep_exif: bool = True,
) -> Optional[Path]:
    """Sequence: *resize* then *compress* and return final JPEG path."""
    resized = resize_image(path, size, keep_exif=keep_exif)
    if resized is None:
        return None
    return compress_image(resized, quality, keep_exif=keep_exif)
