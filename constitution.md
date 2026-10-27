# Constitution — Textile Design Studio (Streamlit)

Last updated: 2026-10-27

## Product Intent
A professional Streamlit application for textile and surface designers. Users can:
- Preview and convert SVG designs
- View seamless/repeat patterns with interactive tiling controls
- Chat with an AI design agent (Gemini) to generate new SVG patterns
- Run a multi-agent quality pipeline (Designer → Reviewer → Preview Checker)
- Save designs to a personal gallery
- Create and schedule automations that generate designs and deliver them via WhatsApp or Telegram

## Stack (locked)
- Language: Python 3.11+
- UI: Streamlit (latest stable)
- LLM orchestration: LangChain (preferred) + LangGraph for multi-agent loops
- Primary LLM provider: Google Gemini
- Image / SVG: Pillow + cairosvg (with pure-Python fallback)
- Scheduling: APScheduler or equivalent background pattern
- Messaging: WhatsApp Business Cloud API + Telegram Bot API (user tokens)
- Persistence (v1): SQLite for gallery + automations
- No React, no heavy custom JS frameworks

Forbidden:
- Emojis in code, UI labels, commits, or skill files
- AI-looking comments or docstrings
- Storing API keys or full conversation history in plain text without protection
- Writing user SVG content to permanent public locations without explicit action
- Blocking Streamlit main thread with long agent runs

## Code Style (Human Expert)
- Clean, professional, readable Python
- Type hints on public functions
- No comments that restate the obvious
- Meaningful names
- Prefer pure functions; session_state usage must be explicit and documented
- Max function length ~40 lines
- Zero dead code

## UI / UX Rules
- Light theme only in this version
- Professional color palette guided by color-theory-master skill
- Excellent spacing, hierarchy, and feedback states
- Chat must feel like a modern professional tool (copy, retry on network error, clear status)
- Repeat pattern viewer must make the tiling effect obvious when density changes

## Architecture Rules
- Single entry point: app/main.py or streamlit_app.py
- Clear package separation:
  - src/svg/          → loader, validator, exporter, preview, repeat
  - src/chat/         → conversation, providers, memory
  - src/agents/       → designer, reviewer, preview_checker, graph
  - src/gallery/      → storage and retrieval
  - src/automation/   → scheduler, runners, messengers
  - src/skills/       → textile design skill package
- Every multi-file change must update docs/CODE_CONNECTION_MAP.md

## Security & Privacy
- Process as much as possible in memory
- API keys live only in Streamlit secrets or encrypted local store
- No telemetry
- User designs leave the machine only when the user explicitly triggers share

## Agent & Skill Rules
- Designer agent must load and follow the textile design skill
- No design is accepted without passing Reviewer + Preview Checker
- Graph / loop must have a hard maximum iteration limit

## Testing & Quality
- Unit tests for pure logic
- Manual acceptance checklist for every major feature
- Connection map must stay accurate

## Agent Behavior Rules
1. Spec is source of truth. Update the relevant spec before changing behavior.
2. Consult and update CODE_CONNECTION_MAP.md on every code change.
3. Never invent requirements.
4. One task at a time.
5. Human approval gate after each major phase document.
