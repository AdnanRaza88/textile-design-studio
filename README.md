# Textile Design Studio

Professional Streamlit application for textile and surface pattern designers.

Preview SVG designs, explore seamless repeats, convert to production formats, and generate new patterns with AI.

## Features (Phase 1)

- Upload SVG files or paste raw SVG code
- Live preview with zoom controls
- Repeat Pattern viewer with interactive density slider
- Export to PNG (transparent), JPG (custom background), WebP and original SVG
- Custom output dimensions or scale multipliers
- Clean light theme and professional UI

## Coming Next

- Chat interface powered by Gemini
- Multi-agent design pipeline (Designer → Reviewer → Preview Checker)
- Personal design gallery
- Scheduled automation with WhatsApp and Telegram delivery

## Quick Start

```bash
git clone https://github.com/AdnanRaza88/textile-design-studio.git
cd textile-design-studio

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app/main.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Project Structure

```
textile-design-studio/
├── app/
│   └── main.py              # Streamlit entry point
├── src/
│   ├── svg/                 # Loader, validator, exporter, repeat
│   ├── chat/                # Conversation system
│   ├── agents/              # Multi-agent pipeline
│   ├── gallery/             # Design gallery
│   ├── automation/          # Scheduler + messengers
│   └── skills/              # Textile design skill
├── requirements.txt
└── README.md
```

## Licence

All rights reserved.
