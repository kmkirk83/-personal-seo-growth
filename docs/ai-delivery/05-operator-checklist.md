# Operator checklist (first vertical slice)

## One-time setup
- [ ] Clone repo and create `.env` from `.env.example`
- [ ] Install Ollama; pull a model that runs on your hardware (`ollama pull llama3.1:8b` or similar)
- [ ] `pip install -r requirements.txt`
- [ ] Shopify: create private/custom app with **only** `read_content` + `write_content`; put token in `.env`
- [ ] Note Shopify Blog ID (`SHOPIFY_BLOG_ID`)
- [ ] Base44: ensure a content/blog surface exists for mynailstudio

## Each article
1. [ ] Pick brand + topic + keyword
2. [ ] `python scripts/generate_article.py --brand ... --topic "..." --keyword "..."`
3. [ ] Review Markdown (facts, voice, links, meta)
4. [ ] Edit in place under `articles/<brand>/`
5. [ ] Shopify (caebikes): `python scripts/publish_shopify_draft.py articles/caebikes/<file>.md --blog-id $SHOPIFY_BLOG_ID`
6. [ ] Confirm draft in Shopify Admin — do **not** publish live until ready
7. [ ] Base44 (mynailstudio): follow `scripts/stage_base44.md`
8. [ ] Update `logs/article-log.md` status if needed

## Safety
- Draft only by default
- No secrets in git
- Rollback = delete draft in Shopify or revert Markdown commit
