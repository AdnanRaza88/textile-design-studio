from __future__ import annotations

import re
from typing import Optional, Tuple
from xml.etree import ElementTree as ET


def format_file_size(num_bytes: int) -> str:
    if num_bytes < 1024:
        return f"{num_bytes} B"
    if num_bytes < 1024 * 1024:
        return f"{num_bytes / 1024:.1f} KB"
    return f"{num_bytes / (1024 * 1024):.1f} MB"


def parse_svg_dimensions(svg_content: str) -> Tuple[int, int]:
    """Extract width/height from viewBox or width/height attributes. Fallback 600x600."""
    try:
        # Remove XML declaration noise for parsing
        clean = re.sub(r"<\?xml[^>]*\?>", "", svg_content, count=1).strip()
        root = ET.fromstring(clean)

        # Prefer viewBox
        view_box = root.get("viewBox") or root.get("viewbox")
        if view_box:
            parts = re.split(r"[,\s]+", view_box.strip())
            if len(parts) >= 4:
                w = int(float(parts[2]))
                h = int(float(parts[3]))
                if w > 0 and h > 0:
                    return w, h

        # Fall back to width / height attributes
        w_attr = root.get("width")
        h_attr = root.get("height")
        if w_attr and h_attr:
            w = int(float(re.sub(r"[^\d.]", "", w_attr)))
            h = int(float(re.sub(r"[^\d.]", "", h_attr)))
            if w > 0 and h > 0:
                return w, h
    except Exception:
        pass

    return 600, 600


def safe_filename(name: str) -> str:
    name = name.strip() or "design"
    name = re.sub(r"[^\w\-. ]", "", name)
    return name[:80] or "design"
