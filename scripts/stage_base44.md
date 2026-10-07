# W5 — Base44 staging path (mynailstudio)

Base44 does not expose a stable public content API comparable to Shopify Admin.
Staging is intentional and manual/Git-assisted.

## Recommended flow

1. Generate article:
   ```bash
   python scripts/generate_article.py --brand mynailstudio --topic "How to apply chrome press-on nails" --keyword "chrome press on nails"
   ```
2. Review/edit the Markdown under `articles/mynailstudio/`.
3. In Base44 AI chat / builder, create or open a Blog / Content surface if one does not exist.
4. Paste the article body (convert Markdown → rich text if the editor requires it).
5. Keep status as draft/unpublished until you approve.
6. Optionally commit the Markdown so GitHub remains the source of truth.

## Optional GitHub sync idea

If Base44 later supports content from a repo, point it at `articles/mynailstudio/`. Until then, treat this folder as the staging queue.
