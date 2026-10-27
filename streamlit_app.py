"""Root entry point for Streamlit Cloud and local runs.

On Streamlit Community Cloud set Main file path to: streamlit_app.py
"""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

# Import only after path is fixed
from app.main import main

main()
