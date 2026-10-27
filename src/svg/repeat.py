from __future__ import annotations

import io
from typing import Optional, Tuple

from PIL import Image

from src.svg.exporter import export_png


def render_repeat_pattern(
    svg_content: str,
    original_width: int,
    original_height: int,
    density: int = 3,
    canvas_size: int = 720,
) -> Tuple[Optional[bytes], str]:
    """
    Tile the SVG into a square canvas.
    density=1 → one large motif
    density=4 → 4x4 grid of smaller motifs
    """
    density = max(1, min(density, 12))

    tile_w = max(1, canvas_size // density)
    tile_h = max(1, canvas_size // density)

    # Render one clean tile
    tile_bytes, err = export_png(svg_content, tile_w, tile_h)
    if err:
        return None, err

    try:
        tile = Image.open(io.BytesIO(tile_bytes)).convert("RGBA")
        canvas = Image.new("RGBA", (canvas_size, canvas_size), (255, 255, 255, 0))

        for row in range(density):
            for col in range(density):
                x = col * tile_w
                y = row * tile_h
                # Handle last column/row sizing if not perfect division
                w = min(tile_w, canvas_size - x)
                h = min(tile_h, canvas_size - y)
                if w != tile_w or h != tile_h:
                    piece = tile.resize((w, h), Image.Resampling.LANCZOS)
                else:
                    piece = tile
                canvas.paste(piece, (x, y), piece)

        buf = io.BytesIO()
        canvas.save(buf, format="PNG")
        return buf.getvalue(), ""
    except Exception as exc:
        return None, str(exc)
