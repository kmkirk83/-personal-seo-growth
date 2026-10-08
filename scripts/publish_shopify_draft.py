#!/usr/bin/env python3
"""
W4: Publish a Markdown article as a Shopify *draft* blog article.
Requires SHOPIFY_SHOP + SHOPIFY_ACCESS_TOKEN in .env (write_content scope).
Never publishes live without a separate human step.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

try:
    import requests
    import markdown as md
except ImportError:
    print("Install dependencies: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]


def load_env() -> None:
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def parse_front_matter(text: str) -> tuple[dict, str]:
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = {}
    for line in parts[1].strip().splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"').strip("'")
    return meta, parts[2].lstrip("\n")


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser(description="Create Shopify draft from Markdown")
    parser.add_argument("markdown_file", type=Path)
    parser.add_argument("--blog-id", default=os.getenv("SHOPIFY_BLOG_ID", ""), help="Numeric blog ID")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    shop = os.getenv("SHOPIFY_SHOP", "").replace("https://", "").rstrip("/")
    token = os.getenv("SHOPIFY_ACCESS_TOKEN", "")
    if not shop or not token:
        print("Set SHOPIFY_SHOP and SHOPIFY_ACCESS_TOKEN in .env", file=sys.stderr)
        sys.exit(1)
    if not args.blog_id:
        print("Pass --blog-id or set SHOPIFY_BLOG_ID (Admin → Online Store → Blog → ID in URL)", file=sys.stderr)
        sys.exit(1)

    raw = args.markdown_file.read_text()
    meta, body_md = parse_front_matter(raw)
    title = meta.get("title") or args.markdown_file.stem
    html = md.markdown(body_md, extensions=["extra", "sane_lists"])

    payload = {
        "article": {
            "title": title,
            "author": meta.get("author", "CA EBIKES DIRECT"),
            "tags": meta.get("keyword", ""),
            "body_html": html,
            "published": False,  # draft only
            "summary_html": meta.get("meta_description", ""),
        }
    }

    if args.dry_run:
        print(json_dumps := __import__("json").dumps(payload, indent=2)[:2000])
        return

    url = f"https://{shop}/admin/api/2024-10/blogs/{args.blog_id}/articles.json"
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json",
    }
    r = requests.post(url, headers=headers, json=payload, timeout=60)
    if r.status_code >= 400:
        print(f"Shopify error {r.status_code}: {r.text}", file=sys.stderr)
        sys.exit(1)
    art = r.json().get("article", {})
    aid = art.get("id")
    print(f"Draft created id={aid}")
    print(f"Admin: https://{shop}/admin/articles/{aid}")


if __name__ == "__main__":
    main()
