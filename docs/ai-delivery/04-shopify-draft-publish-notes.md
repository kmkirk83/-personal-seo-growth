# Shopify Draft Publish Notes

Informed by Omnibuild operational patterns and Shopify Admin API constraints.

## Principles
1. **Draft-first** — every automated publish creates a draft article only.
2. **Minimal scopes** — private/custom app with `read_content` + `write_content` only.
3. **Human gate** — operator must explicitly approve before setting published status.
4. **Secrets local** — token only in `.env`, never committed.
5. **Fail closed** — if token missing or API error, stop and log; do not retry blindly.

## Recommended mutation flow
1. Convert Markdown article → HTML body.
2. Call `articleCreate` (or REST equivalent) with `isPublished: false` / draft.
3. Return admin URL + article ID to operator.
4. Operator reviews in Shopify admin.
5. Optional separate script or manual step sets published = true.

## Verification ideas (later)
- cartverity-style Playwright check that draft exists in admin or public URL 404 until published.
- Log article ID + timestamp in `logs/article-log.md`.

## Out of scope for first vertical slice
- Automatic live publish
- Multi-blog routing complexity
- Image CDN upload automation (can be manual for first articles)
