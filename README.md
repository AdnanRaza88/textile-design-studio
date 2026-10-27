# Textile Design Studio

Professional Streamlit application for textile and surface pattern designers.

Preview SVG designs, explore seamless repeats, convert to production formats, and chat with a Gemini-powered design assistant.

## Features

- Upload SVG files or paste raw SVG code
- Live preview with zoom controls
- Repeat Pattern viewer with interactive density slider
- Export to PNG (transparent), JPG (custom background), WebP and original SVG
- Design Chat powered by Gemini
- Clean light theme and professional UI

## Quick Start (local)

```bash
git clone https://github.com/AdnanRaza88/textile-design-studio.git
cd textile-design-studio

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run streamlit_app.py
```

Or:

```bash
streamlit run app/main.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Streamlit Community Cloud

1. Deploy from this repository.
2. Set **Main file path** to:

```
streamlit_app.py
```

3. (Optional) Add secret `GEMINI_API_KEY` under App settings → Secrets for the Chat tab.

## Project Structure

```
textile-design-studio/
├── streamlit_app.py         # Preferred entry point (Cloud + local)
├── app/
│   └── main.py              # App logic
├── src/
│   ├── svg/                 # Loader, validator, exporter, repeat
│   ├── chat/                # Conversation system + Gemini
│   ├── agents/              # Multi-agent pipeline (next)
│   ├── gallery/             # Design gallery (next)
│   ├── automation/          # Scheduler + messengers (next)
│   └── skills/              # Textile design skill
├── requirements.txt
└── README.md
```

## Licence

All rights reserved.
