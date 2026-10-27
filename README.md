# Textile Design Studio

Professional Streamlit application for textile and surface pattern designers.

Preview SVG designs, explore seamless repeats, convert to production formats, and (in upcoming modules) generate new patterns with a multi-agent AI pipeline powered by Gemini and a specialised textile design skill.

## Current Features (Phase 1)

- Upload SVG files or paste raw SVG code
- Live preview with zoom controls
- **Repeat Pattern viewer** – interactive density slider that tiles the design (higher density = more smaller motifs)
- Export to PNG (transparent), JPG (custom background), WebP and original SVG
- Custom output dimensions or scale multipliers
- Clean light theme, professional UI, zero visual noise

## Planned Modules

| Module | Status | Description |
|--------|--------|-------------|
| Core SVG Studio + Repeat | Done | Preview, convert, tile patterns |
| Chat System (Gemini) | Next | Professional conversation UI with copy / retry |
| Multi-Agent Pipeline | Next | Designer → Reviewer → Preview Checker (LangGraph) |
| Textile Design Skill | Included | High-quality skill that drives the Designer agent |
| Gallery | Planned | Save, browse and reload designs |
| Automation | Planned | Scheduled generation + WhatsApp / Telegram delivery |

## Quick Start

```bash
# Clone
git clone https://github.com/AdnanRaza88/textile-design-studio.git
cd textile-design-studio

# Install
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Run
streamlit run app/main.py
```

Open the URL shown in the terminal (usually http://localhost:8501).

## Project Structure

```
textile-design-studio/
├── app/
│   └── main.py                 # Streamlit entry point
├── src/
│   ├── svg/                    # Loader, validator, exporter, repeat
│   ├── chat/                   # Conversation system (coming)
│   ├── agents/                 # Multi-agent pipeline (coming)
│   ├── gallery/                # Design gallery (coming)
│   ├── automation/             # Scheduler + messengers (coming)
│   └── skills/
│       └── textile_design_skill.md
├── specs/                      # Spec-driven development documents
├── docs/
│   └── CODE_CONNECTION_MAP.md
├── constitution.md
├── requirements.txt
└── README.md
```

## Spec-Driven Development

This project follows a strict Spec-Driven Development workflow:

1. **Constitution** – non-negotiable rules (stack, style, privacy)
2. **Specs** – what and why (user stories, acceptance criteria)
3. **Design** – how (architecture, data models)
4. **Tasks** – ordered implementation steps
5. **Code** – only after the above are approved
6. **Connection Map** – living graph of every file relationship

See the `specs/` and `docs/` folders.

## Textile Design Skill

The file `src/skills/textile_design_skill.md` is a complete, portable skill that any capable model can use to generate production-ready seamless SVG textile patterns. It is the knowledge base the Designer agent will load.

## Licence

Private / All rights reserved for now. Contact the author for usage rights.

---

Built with care for professional textile designers.
