from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.svg.utils import format_file_size, parse_svg_dimensions
from src.svg.validator import validate_svg_content


@dataclass
class SvgDocument:
    content: str
    source_type: str  # "file" | "code"
    file_name: str
    file_size: int
    width: int
    height: int

    @property
    def size_label(self) -> str:
        return format_file_size(self.file_size)


def load_from_string(
    content: str,
    source_type: str = "code",
    file_name: str = "svg-code",
) -> tuple[Optional[SvgDocument], str]:
    ok, msg = validate_svg_content(content)
    if not ok:
        return None, msg

    width, height = parse_svg_dimensions(content)
    size = len(content.encode("utf-8"))

    doc = SvgDocument(
        content=content.strip(),
        source_type=source_type,
        file_name=file_name,
        file_size=size,
        width=width,
        height=height,
    )
    return doc, ""


def load_from_upload(uploaded_file) -> tuple[Optional[SvgDocument], str]:
    if uploaded_file is None:
        return None, "No file provided."

    try:
        raw = uploaded_file.getvalue()
        content = raw.decode("utf-8")
    except Exception:
        return None, "Could not read the uploaded file as text."

    name = uploaded_file.name or "upload.svg"
    if name.lower().endswith(".svg"):
        name = name[:-4]

    return load_from_string(content, source_type="file", file_name=name)
