"""Root entry point for Streamlit Cloud and local runs."""
from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app.main import main

if __name__ == "__main__":
    main()
else:
    # When Streamlit loads this file it executes top-level code
    main()
