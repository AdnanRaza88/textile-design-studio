from __future__ import annotations

import io
from typing import Optional, Tuple

from PIL import Image

try:
    import cairosvg
    HAS_CAIRO = True
except Exception:
    HAS_CAIRO = False


def _svg_to_png_bytes(svg_content: str, width: int, height: int) -> bytes:
    errors = []

    if HAS_CAIRO:
        try:
            return cairosvg.svg2png(
                bytestring=svg_content.encode("utf-8"),
                output_width=width,
                output_height=height,
            )
        except Exception as exc:
            errors.append(f"cairosvg: {exc}")

    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM

        drawing = svg2rlg(io.BytesIO(svg_content.encode("utf-8")))
        if drawing is None:
            raise RuntimeError("svglib could not parse SVG")
        scale_x = width / drawing.width if drawing.width else 1
        scale_y = height / drawing.height if drawing.height else 1
        drawing.width = width
        drawing.height = height
        drawing.scale(scale_x, scale_y)
        return renderPM.drawToString(drawing, fmt="PNG")
    except Exception as exc:
        errors.append(f"svglib: {exc}")

    detail = "; ".join(errors) if errors else "unknown"
    raise RuntimeError(
        "Could not rasterize SVG for export. "
        "On Streamlit Cloud, ensure packages.txt includes Cairo libraries. "
        f"Details: {detail}"
    )


def export_png(
    svg_content: str,
    width: int,
    height: int,
) -> Tuple[Optional[bytes], str]:
    try:
        data = _svg_to_png_bytes(svg_content, width, height)
        return data, ""
    except Exception as exc:
        return None, str(exc)


def export_jpg(
    svg_content: str,
    width: int,
    height: int,
    background: str = "#ffffff",
    quality: int = 92,
) -> Tuple[Optional[bytes], str]:
    png_bytes, err = export_png(svg_content, width, height)
    if err:
        return None, err

    try:
        img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
        bg = Image.new("RGB", img.size, background)
        bg.paste(img, mask=img.split()[3])
        buf = io.BytesIO()
        bg.save(buf, format="JPEG", quality=quality)
        return buf.getvalue(), ""
    except Exception as exc:
        return None, str(exc)


def export_webp(
    svg_content: str,
    width: int,
    height: int,
    quality: int = 90,
) -> Tuple[Optional[bytes], str]:
    png_bytes, err = export_png(svg_content, width, height)
    if err:
        return None, err

    try:
        img = Image.open(io.BytesIO(png_bytes))
        buf = io.BytesIO()
        img.save(buf, format="WEBP", quality=quality)
        return buf.getvalue(), ""
    except Exception as exc:
        return None, str(exc)


def export_svg_bytes(svg_content: str) -> bytes:
    return svg_content.encode("utf-8")
