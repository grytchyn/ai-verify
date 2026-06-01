# AI Verify — EU AI Act Compliance Checker

A SaaS MVP that automatically checks whether a website or AI system complies with the **EU AI Act**, providing instant analysis and recommendations in **5 languages** (EN/DE/FR/IT/ES).

**Live:** https://ai-act-verify.onrender.com  
**Repository:** https://github.com/grytchyn/ai-verify  
**Design Bible:** `/root/mega/Hermes/projects/ai-verify/DESIGN-BIBLE.md`  
**Dev Bible:** `/root/mega/Hermes/projects/ai-verify/DEV-BIBLE.md`

---

## Features

- **Multi-language** — Full UI and reports in English, German, French, Italian, Spanish
- **EU AI Act compliance check** — Classifies AI systems by risk level per Articles 5–20
- **Automated scoring** — Weighted compliance score (0–100) based on regulatory factors
- **LLM-powered analysis** — Uses **Mistral AI's Ministral 3:8b** 🇫🇷 (European model) for report generation
- **Google Sign-In** — Save and view your compliance report history
- **Instant results** — Report generated in seconds
- **Dark theme** — Modern, accessible dark UI with design tokens throughout

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | Python 3.11+ / Flask |
| **Database** | PostgreSQL (Render managed) |
| **Auth** | Google OAuth 2.0 (GSI) |
| **LLM** | **Ministral 3:8b** via Ollama Cloud (Mistral AI, Paris 🇫🇷) |
| **Web Search** | Tavily API |
| **Frontend** | Vanilla HTML + CSS + JS (no framework) |
| **Hosting** | Render (auto-deploy from `main`) |

### European AI Model 🇪🇺

We use **Ministral 3:8b** by **Mistral AI** (headquartered in Paris, France) for all AI-powered compliance analysis. This means:

- ✅ Fully compliant with EU data protection standards
- ✅ No data transfer outside the European Union
- ✅ Excellent multilingual support (all 5 target languages)
- ✅ Transparent and auditable AI processing

## Architecture

### Shared CSS (Single Source of Truth)

All 3 pages pull shared component styles from **`/static/components.css`**:

```
/static/components.css   → Shared: design tokens, nav, buttons, auth, forms, footer
/static/index.html       → Landing page (page-specific: hero, features, FAQ)
/static/submit.html      → Compliance form (page-specific: multiselect, progress bar)
/static/result.html      → Report page (page-specific: score ring, infographic, neural loading)
```

Every color, spacing, and component is defined once in `components.css` — change it there, it updates everywhere.

### Languages

- **5 supported:** English, Deutsch, Français, Italiano, Español
- **Persisted via:** `localStorage` + URL parameter `?lang=`
- **UI translated via:** `data-i18n` attributes + JS translation objects
- **LLM instructed via:** Language-specific system prompts sent as `role: "system"`

## Getting Started

### Prerequisites

- Python 3.11+
- Ollama with Ministral 3:8b:
  ```bash
  ollama pull ministral-3:8b
  ```

### Local Development

```bash
git clone https://github.com/grytchyn/ai-verify.git
cd ai-verify
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # configure your env vars
python -m app.main
```

### Environment Variables

```
OLLAMA_API_BASE=https://ollama.com/v1/chat/completions
OLLAMA_MODEL=ministral-3:8b
OLLAMA_API_KEY=your_key
DATABASE_URL=postgresql://...
GOOGLE_CLIENT_ID=your_client_id
```

## Project Structure

```
/root/ai-verify/
├── app/
│   ├── main.py          # Flask routes
│   ├── llm.py           # Ministral 3:8b via Ollama API
│   ├── prompts.py       # Prompt templates (5 languages)
│   ├── scoring.py       # Compliance scoring engine
│   ├── auth.py          # Google OAuth
│   ├── database.py      # SQLAlchemy + PostgreSQL
│   └── models.py        # DB models
├── static/
│   ├── components.css   # Shared styles (single source of truth)
│   ├── index.html       # Landing page
│   ├── submit.html      # Compliance form
│   ├── result.html      # Report page
│   ├── auth.js          # Google OAuth client
│   ├── favicon.svg      # Shield logo
│   └── og-image.png     # Social preview
├── Dockerfile
├── requirements.txt
└── README.md
```

## How It Works

1. User selects their language and fills out the compliance form
2. Form data is validated and cached in `localStorage`
3. Backend calculates a compliance score using the scoring engine
4. LLM (Ministral 3:8b) generates a detailed analysis in the selected language
5. Report is rendered with score ring, infographic sections, and recommendations
6. Signed-in users can save reports to their profile

## License

MIT