# Personal SEO Growth Engine

Zero-recurring-cost AI content system for:
- https://mynailstudio.base44.app (Nail Studio)
- https://caebikesdirect.myshopify.com (CA EBIKES DIRECT)

Built under the Autonomous AI Build Playbook. First vertical slice is production-ready for local generation + Shopify draft publish.

## Quick Start

```bash
git clone https://github.com/kmkirk83/-personal-seo-growth.git
cd -- -personal-seo-growth
cp .env.example .env   # add Shopify token + blog id when ready
pip install -r requirements.txt
# Install Ollama and: ollama pull llama3.1:8b
```

### Generate an article

```bash
python scripts/generate_article.py --brand caebikes --topic "Mid-drive vs hub motor kits" --keyword "mid drive conversion kit"
python scripts/generate_article.py --brand mynailstudio --topic "Chrome press-on nails at home" --keyword "chrome press on nails"
```

### Publish Shopify draft (caebikes)

```bash
python scripts/publish_shopify_draft.py articles/caebikes/YOUR-FILE.md --blog-id $SHOPIFY_BLOG_ID
```

### Stage Base44 (mynailstudio)

See `scripts/stage_base44.md`.

## Structure

```
brands/           # Brand voice, products, audience
articles/         # Generated + sample Markdown
scripts/          # generate_article.py, publish_shopify_draft.py
docs/ai-delivery/ # Contract, ADR, checklist, portfolio map
logs/             # article-log.md
```

## Safety

- Publishes are **draft only**
- Human approval before live
- Secrets only in `.env`
- No paid APIs required

## Operator checklist

See `docs/ai-delivery/05-operator-checklist.md`.
