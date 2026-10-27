from __future__ import annotations

import re


def _ensure_svg_sizing(svg_content: str, max_width: int = 720, max_height: int = 720) -> str:
    """Inject max-width/height styles so the SVG scales in the browser."""
    svg = svg_content.strip()

    def inject_style(match: re.Match) -> str:
        tag = match.group(0)
        style_bits = f"max-width:{max_width}px;max-height:{max_height}px;width:100%;height:auto;"
        if re.search(r"\sstyle=", tag, re.IGNORECASE):
            return re.sub(
                r'style=(["\'])(.*?)\1',
                lambda m: f'style={m.group(1)}{style_bits}{m.group(2)}{m.group(1)}',
                tag,
                count=1,
                flags=re.IGNORECASE,
            )
        return tag[:-1] + f' style="{style_bits}">'

    return re.sub(r"<svg\b[^>]*>", inject_style, svg, count=1, flags=re.IGNORECASE)


def svg_to_html_preview(svg_content: str, max_width: int = 720, max_height: int = 720) -> str:
    """Return HTML that renders the SVG natively in the browser (no rasterizer)."""
    sized = _ensure_svg_sizing(svg_content, max_width=max_width, max_height=max_height)
    return f"""
    <div style="
        display:flex;
        align-items:center;
        justify-content:center;
        min-height:200px;
        max-height:{max_height + 40}px;
        overflow:auto;
        padding:16px;
        border-radius:12px;
        border:1px solid rgba(124,58,237,0.12);
        background:
            linear-gradient(45deg, #e8e6f0 25%, transparent 25%),
            linear-gradient(-45deg, #e8e6f0 25%, transparent 25%),
            linear-gradient(45deg, transparent 75%, #e8e6f0 75%),
            linear-gradient(-45deg, transparent 75%, #e8e6f0 75%);
        background-size:16px 16px;
        background-position:0 0, 0 8px, 8px -8px, -8px 0;
        background-color:#f5f3fa;
    ">
        {sized}
    </div>
    """


def svg_repeat_html(
    svg_content: str,
    density: int = 3,
    canvas_size: int = 720,
) -> str:
    """Tile the same SVG in an HTML grid — no server-side rasterizer needed."""
    density = max(1, min(int(density), 12))
    cell = max(24, canvas_size // density)
    cell_svg = _ensure_svg_sizing(svg_content, max_width=cell, max_height=cell)
    cell_svg = re.sub(
        r'style=(["\'])(.*?)\1',
        lambda m: f'style={m.group(1)}width:{cell}px;height:{cell}px;display:block;{m.group(2)}{m.group(1)}',
        cell_svg,
        count=1,
        flags=re.IGNORECASE,
    )
    tiles = "".join(
        f'<div style="width:{cell}px;height:{cell}px;overflow:hidden;">{cell_svg}</div>'
        for _ in range(density * density)
    )
    return f"""
    <div style="
        display:grid;
        grid-template-columns:repeat({density}, {cell}px);
        width:{density * cell}px;
        max-width:100%;
        overflow:auto;
        margin:0 auto;
        border-radius:12px;
        border:1px solid rgba(124,58,237,0.12);
        background:#f5f3fa;
    ">
        {tiles}
    </div>
    """
