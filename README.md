# Personal SEO Growth Engine

Zero-recurring-cost AI content system for:
- https://mynailstudio.base44.app (Nail Studio)
- https://caebikesdirect.myshopify.com (California eBikes / eBike Super Shop)

Built under the Autonomous AI Build Playbook.

## Quick Start

1. Copy `.env.example` to `.env` and fill in secrets (never commit `.env`).
2. Install Ollama and pull a model that runs well on your hardware.
3. Place brand context in `brands/`.
4. Run generation scripts from `scripts/`.
5. Review Markdown articles in `articles/` before any publish.

## Structure

```
brands/           # Brand voice, products, audience notes
articles/         # Generated Markdown articles (by brand)
scripts/          # Generation + Shopify draft publisher
docs/ai-delivery/ # Outcome Contract, ADR, change records
logs/             # Simple article status log
```

## Safety Rules

- All publishes start as **draft**.
- Human approval required before going live.
- Secrets stay in `.env` only.
- No paid APIs required.
