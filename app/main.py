from __future__ import annotations

import io
import streamlit as st
from PIL import Image

from src.svg.loader import load_from_string, load_from_upload, SvgDocument
from src.svg.exporter import export_png, export_jpg, export_webp, export_svg_bytes
from src.svg.repeat import render_repeat_pattern
from src.svg.utils import safe_filename


st.set_page_config(
    page_title="Textile Design Studio",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# Custom light theme styling
# ---------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* Clean professional light theme */
    .stApp {
        background: linear-gradient(160deg, #f8f7fc 0%, #f0eef8 40%, #eef6f9 100%);
    }
    h1, h2, h3 {
        color: #2d2b3d !important;
        font-weight: 700 !important;
        letter-spacing: -0.3px;
    }
    .block-container {
        padding-top: 1.5rem;
        max-width: 1100px;
    }
    div[data-testid="stMetric"] {
        background: rgba(255,255,255,0.7);
        border-radius: 12px;
        padding: 8px 12px;
        border: 1px solid rgba(124,58,237,0.12);
    }
    .stButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def init_state():
    defaults = {
        "doc": None,
        "zoom": 1.0,
        "scale": 1.0,
        "custom_w": None,
        "custom_h": None,
        "bg_color": "#ffffff",
        "view_mode": "single",  # single | repeat
        "density": 3,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


def reset_all():
    for key in list(st.session_state.keys()):
        if key.startswith("FormSubmitter") or key.startswith("file_uploader"):
            continue
        del st.session_state[key]
    init_state()


def get_output_dims(doc: SvgDocument) -> tuple[int, int]:
    custom_w = st.session_state.get("custom_w")
    custom_h = st.session_state.get("custom_h")
    if custom_w or custom_h:
        aspect = doc.width / doc.height if doc.height else 1
        if custom_w and custom_h:
            return int(custom_w), int(custom_h)
        if custom_w:
            return int(custom_w), max(1, int(custom_w / aspect))
        return max(1, int(custom_h * aspect)), int(custom_h)

    scale = st.session_state.scale
    return max(1, int(doc.width * scale)), max(1, int(doc.height * scale))


def main():
    init_state()

    st.title("Textile Design Studio")
    st.caption("Preview, convert and explore seamless SVG patterns for textile design")

    # ------------------------------------------------------------------
    # Sidebar – global actions
    # ------------------------------------------------------------------
    with st.sidebar:
        st.header("Workspace")
        if st.button("Reset everything", use_container_width=True):
            reset_all()
            st.rerun()

        st.divider()
        st.markdown("**Modules (coming)**")
        st.markdown("- Chat + Gemini")
        st.markdown("- Multi-Agent Designer")
        st.markdown("- Gallery")
        st.markdown("- Automation + WhatsApp / Telegram")

    # ------------------------------------------------------------------
    # Input section
    # ------------------------------------------------------------------
    tab_upload, tab_code = st.tabs(["Upload File", "Paste Code"])

    with tab_upload:
        uploaded = st.file_uploader(
            "Drop an SVG file",
            type=["svg"],
            accept_multiple_files=False,
            key="uploader",
        )
        if uploaded is not None:
            doc, err = load_from_upload(uploaded)
            if err:
                st.error(err)
            else:
                st.session_state.doc = doc
                st.success(f"Loaded {doc.file_name}")

    with tab_code:
        code = st.text_area(
            "Paste SVG code",
            height=220,
            placeholder="Paste your <svg>...</svg> here",
            key="code_area",
        )
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Preview Code", type="primary", use_container_width=True):
                doc, err = load_from_string(code, source_type="code", file_name="svg-code")
                if err:
                    st.error(err)
                else:
                    st.session_state.doc = doc
                    st.success("SVG code loaded")
        with col_b:
            if st.button("Load Sample", use_container_width=True):
                sample = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="200" height="200">
  <defs>
    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#7c3aed"/>
      <stop offset="100%" style="stop-color:#ec4899"/>
    </linearGradient>
  </defs>
  <circle cx="100" cy="100" r="80" fill="url(#g1)" opacity="0.9"/>
  <circle cx="70" cy="80" r="30" fill="white" opacity="0.3"/>
  <path d="M 60 120 Q 100 80 140 120 Q 100 160 60 120" fill="white" opacity="0.4"/>
  <text x="100" y="110" text-anchor="middle" fill="white" font-size="20" font-family="Arial" font-weight="bold">SVG</text>
</svg>'''
                doc, err = load_from_string(sample, source_type="code", file_name="sample")
                if not err:
                    st.session_state.doc = doc
                    st.session_state.code_area = sample
                    st.rerun()

    doc: SvgDocument | None = st.session_state.doc

    if doc is None:
        st.info("Upload an SVG file or paste SVG code to begin.")
        return

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Source", "File" if doc.source_type == "file" else "Code")
    m2.metric("Name", doc.file_name)
    m3.metric("Size", doc.size_label)
    m4.metric("Dimensions", f"{doc.width} × {doc.height}")

    st.divider()

    # ------------------------------------------------------------------
    # View mode
    # ------------------------------------------------------------------
    view_cols = st.columns([1, 1, 2])
    with view_cols[0]:
        mode = st.radio(
            "View mode",
            options=["Single Preview", "Repeat Pattern"],
            horizontal=True,
            key="view_radio",
        )
        st.session_state.view_mode = "single" if mode.startswith("Single") else "repeat"

    # ------------------------------------------------------------------
    # Preview area
    # ------------------------------------------------------------------
    left, right = st.columns([3, 2])

    with left:
        st.subheader("Live Preview")

        if st.session_state.view_mode == "single":
            zoom_c1, zoom_c2, zoom_c3, zoom_c4 = st.columns([1, 1, 1, 2])
            with zoom_c1:
                if st.button("−", key="zoom_out"):
                    st.session_state.zoom = max(0.25, st.session_state.zoom - 0.25)
            with zoom_c2:
                st.write(f"**{int(st.session_state.zoom * 100)}%**")
            with zoom_c3:
                if st.button("+", key="zoom_in"):
                    st.session_state.zoom = min(5.0, st.session_state.zoom + 0.25)
            with zoom_c4:
                if st.button("Reset Zoom"):
                    st.session_state.zoom = 1.0

            # Render single preview
            disp_w = max(64, int(doc.width * st.session_state.zoom))
            disp_h = max(64, int(doc.height * st.session_state.zoom))
            png_bytes, err = export_png(doc.content, disp_w, disp_h)
            if err:
                st.error(f"Could not render preview: {err}")
            else:
                st.image(png_bytes, use_container_width=False)

        else:
            # Repeat pattern view
            density = st.slider(
                "Repeat density (tiles per side)",
                min_value=1,
                max_value=10,
                value=st.session_state.density,
                help="Higher value = more smaller copies. Lower value = fewer larger copies.",
            )
            st.session_state.density = density

            canvas_size = 720
            pattern_bytes, err = render_repeat_pattern(
                doc.content,
                doc.width,
                doc.height,
                density=density,
                canvas_size=canvas_size,
            )
            if err:
                st.error(f"Could not render repeat pattern: {err}")
            else:
                st.image(pattern_bytes, use_container_width=True)
                st.caption(f"{density}×{density} tile · canvas {canvas_size}px")

    # ------------------------------------------------------------------
    # Export controls
    # ------------------------------------------------------------------
    with right:
        st.subheader("Export")

        scale_options = {
            "Original (1×)": 1.0,
            "0.5×": 0.5,
            "2×": 2.0,
            "3×": 3.0,
            "4×": 4.0,
        }
        chosen = st.selectbox("Scale", list(scale_options.keys()), index=0)
        st.session_state.scale = scale_options[chosen]

        c1, c2 = st.columns(2)
        with c1:
            cw = st.number_input("Custom width (px)", min_value=0, value=0, step=10)
            st.session_state.custom_w = cw if cw > 0 else None
        with c2:
            ch = st.number_input("Custom height (px)", min_value=0, value=0, step=10)
            st.session_state.custom_h = ch if ch > 0 else None

        st.session_state.bg_color = st.color_picker(
            "JPG background",
            value=st.session_state.bg_color,
        )

        out_w, out_h = get_output_dims(doc)
        st.caption(f"Output size: {out_w} × {out_h} px")

        st.divider()

        base_name = safe_filename(doc.file_name)

        # PNG
        png_data, png_err = export_png(doc.content, out_w, out_h)
        if png_data:
            st.download_button(
                "Download PNG",
                data=png_data,
                file_name=f"{base_name}.png",
                mime="image/png",
                use_container_width=True,
            )
        else:
            st.warning(png_err or "PNG export unavailable")

        # JPG
        jpg_data, jpg_err = export_jpg(
            doc.content, out_w, out_h, background=st.session_state.bg_color
        )
        if jpg_data:
            st.download_button(
                "Download JPG",
                data=jpg_data,
                file_name=f"{base_name}.jpg",
                mime="image/jpeg",
                use_container_width=True,
            )
        else:
            st.warning(jpg_err or "JPG export unavailable")

        # WebP
        webp_data, webp_err = export_webp(doc.content, out_w, out_h)
        if webp_data:
            st.download_button(
                "Download WebP",
                data=webp_data,
                file_name=f"{base_name}.webp",
                mime="image/webp",
                use_container_width=True,
            )
        else:
            st.warning(webp_err or "WebP export unavailable")

        # SVG
        svg_bytes = export_svg_bytes(doc.content)
        st.download_button(
            "Download SVG",
            data=svg_bytes,
            file_name=f"{base_name}.svg",
            mime="image/svg+xml",
            use_container_width=True,
        )


if __name__ == "__main__":
    main()
