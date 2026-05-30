# BuildWithAI

An AI-powered agentic framework built on a **3-layer architecture** — combining natural language directives, intelligent orchestration, and deterministic Python scripts to reliably automate complex workflows.

---

## Architecture Overview

```
┌────────────────────────────────────────────────┐
│  Layer 1 · Directives   (directives/)          │
│  Natural language SOPs — the "what to do"      │
├────────────────────────────────────────────────┤
│  Layer 2 · Orchestration   (AI Agent)          │
│  Intelligent routing, error handling, routing  │
├────────────────────────────────────────────────┤
│  Layer 3 · Execution   (execution/)            │
│  Deterministic Python scripts — reliable work  │
└────────────────────────────────────────────────┘
```

> **Why this works:** LLMs are probabilistic — 90% accuracy per step compounds to 50% success over 5 steps. By pushing complexity into deterministic code (Layer 3), the AI agent (Layer 2) only needs to make high-level decisions, dramatically improving reliability.

---

## Directory Structure

```
buildAI/
├── directives/          # Layer 1 — SOPs written in Markdown
├── execution/           # Layer 3 — Deterministic Python scripts
├── brand-guidelines/    # Skill: brand identity & design guidelines
├── brand-scraper/       # Skill: website brand scraping
├── brand_data/          # Scraped brand outputs (colors, fonts, CSS)
├── frontend-design/     # Skill: frontend UI design
├── skill-creator/       # Tooling to create & evaluate new skills
├── website/             # Project website / dashboard UI
├── tmp/                 # Intermediate files (gitignored, regenerated)
├── .env.example         # Environment variable template
├── GEMINI.md            # Agent instructions (Gemini)
├── CLAUDE.md            # Agent instructions (Claude)
└── AGENTS.md            # Agent instructions (generic)
```

---

## Quick Start

### 1. Clone the repo

```bash
git clone https://github.com/Ram-sah19/buildwithai.git
cd buildwithai
```

### 2. Set up your environment

```bash
cp .env.example .env
```

Open `.env` and fill in your API keys:

| Variable | Purpose |
|---|---|
| `OPENAI_API_KEY` | OpenAI API access |
| `ANTHROPIC_API_KEY` | Anthropic / Claude access |
| `GEMINI_API_KEY` | Google Gemini access |
| `FIRECRAWL_API_KEY` | Web scraping via Firecrawl |
| `GOOGLE_APPLICATION_CREDENTIALS` | Google OAuth (path to `credentials.json`) |

### 3. Install Python dependencies

```bash
pip install -r requirements.txt
# Or per-script: pip install firecrawl-py python-dotenv
```

---

## Available Directives & Scripts

### Brand Scraper

Scrape any website to extract a full brand intelligence package — colors, typography, fonts, images, and a CSS starter kit.

```bash
# Basic scrape
python execution/scrape_brand.py --url https://example.com

# Include sub-pages for richer data
python execution/scrape_brand.py --url https://example.com --subpages

# Skip local image downloads
python execution/scrape_brand.py --url https://example.com --no-images
```

**Outputs** (saved to `brand_data/`):
- `brand_report.md` — Human-readable brand summary
- `brand_data.json` — Structured JSON (colors, fonts, components)
- `variables.css` — Ready-to-use CSS custom properties
- `images/` — Downloaded logos, hero images, etc.

See [`directives/scrape_brand.md`](directives/scrape_brand.md) for full details.

---

## Skills

Skills are self-contained modules that extend the agent's capabilities. Each skill lives in its own directory with a `SKILL_*.md` specification file.

| Skill | Directory | Description |
|---|---|---|
| Brand Guidelines | `brand-guidelines/` | Extract & codify brand identity |
| Brand Scraper | `brand-scraper/` | Scrape website brand assets |
| Frontend Design | `frontend-design/` | Generate UI designs from brand data |
| Skill Creator | `skill-creator/` | Build, evaluate & package new skills |

---

## Operating Principles

- **Check for tools first** — before writing a new script, check `execution/` for existing ones.
- **Self-anneal on failure** — when a script breaks, fix it, update the directive, and test again. The system gets stronger with each error.
- **Deliverables live in the cloud** — Google Sheets, Slides, and similar; local files in `tmp/` are intermediates only.

---

## Contributing

1. Fork the repo
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Follow the directive template in [`directives/README.md`](directives/README.md) when adding new workflows
4. Follow the execution script rules in [`execution/README.md`](execution/README.md) when adding new scripts
5. Open a pull request

---

## License

See individual skill directories for their respective licenses.
