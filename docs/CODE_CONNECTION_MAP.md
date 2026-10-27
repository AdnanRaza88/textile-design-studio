# Code Connection Map

Last updated: 2026-10-27 19:30 PKT

## 1. Entry Points
- `app/main.py` — Streamlit application entry (`streamlit run app/main.py`)

## 2. File Inventory

| Path | Role | Key exports | Depends on | Depended by |
|------|------|-------------|------------|-------------|
| app/main.py | UI orchestration | main() | src.svg.* | — |
| src/svg/validator.py | SVG safety checks | is_likely_svg, validate_svg_content, validate_dimensions | — | loader |
| src/svg/utils.py | Helpers | format_file_size, parse_svg_dimensions, safe_filename | — | loader, main |
| src/svg/loader.py | Load & normalise SVG | SvgDocument, load_from_string, load_from_upload | validator, utils | main |
| src/svg/exporter.py | Raster + SVG export | export_png, export_jpg, export_webp, export_svg_bytes | Pillow, cairosvg/svglib | main, repeat |
| src/svg/repeat.py | Tile / repeat pattern | render_repeat_pattern | exporter | main |
| src/skills/textile_design_skill.md | Designer knowledge | (markdown skill) | — | agents (future) |

## 3. Import / Call Graph

### SVG layer
- main → loader.load_from_upload / load_from_string
- main → exporter.export_*
- main → repeat.render_repeat_pattern
- repeat → exporter.export_png
- loader → validator.validate_svg_content
- loader → utils.parse_svg_dimensions / format_file_size

### Shared state (session_state keys)
- doc : SvgDocument | None
- zoom, scale, custom_w, custom_h, bg_color
- view_mode ("single" | "repeat")
- density (int)

## 4. Critical Shared Contracts
- `SvgDocument` dataclass (content, source_type, file_name, file_size, width, height)
- Export functions all return `Tuple[Optional[bytes], str]` (data, error_message)
- Max SVG size: 5 MB (validator)

## 5. Change Impact Rules
- Changing `SvgDocument` fields requires updates in loader + main + any future gallery/automation modules.
- Changing export signatures requires updates in main and repeat.
- Adding new session_state keys must be documented here and initialised in `init_state()`.

## 6. Recent Changes Log
- 2026-10-27: Initial bootstrap – core SVG modules + Streamlit UI + repeat pattern viewer + skill file + connection map created.
