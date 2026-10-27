from __future__ import annotations

import re
from typing import Tuple


MAX_SVG_BYTES = 5 * 1024 * 1024  # 5 MB


def is_likely_svg(content: str) -> bool:
    if not content or not isinstance(content, str):
        return False
    stripped = content.strip()
    return "<svg" in stripped.lower() and "</svg>" in stripped.lower()


def validate_svg_content(content: str) -> Tuple[bool, str]:
    if not content or not content.strip():
        return False, "SVG content is empty."

    size = len(content.encode("utf-8"))
    if size > MAX_SVG_BYTES:
        return False, f"SVG is too large ({size // 1024} KB). Maximum allowed is 5 MB."

    if not is_likely_svg(content):
        return False, "Content does not look like valid SVG (missing <svg> or </svg>)."

    # Basic structural safety
    if re.search(r"<script[\s>]", content, re.IGNORECASE):
        return False, "SVG contains <script> tags which are not allowed."

    return True, ""


def validate_dimensions(width: int | None, height: int | None) -> Tuple[bool, str]:
    if width is not None and width <= 0:
        return False, "Width must be a positive integer."
    if height is not None and height <= 0:
        return False, "Height must be a positive integer."
    return True, ""
