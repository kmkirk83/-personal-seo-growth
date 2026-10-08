#!/usr/bin/env python3
"""
W3: Generate a brand-voiced, SEO-structured Markdown article using local Ollama
(or optional free-cloud fallbacks). Human review required before any publish.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from datetime import date
from pathlib import Path

try:
    import requests
except ImportError:
    print("Install dependencies: pip install -r requirements.txt", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[1]
BRANDS = ROOT / "brands"
ARTICLES = ROOT / "articles"
LOG = ROOT / "logs" / "article-log.md"


def load_env() -> None:
    env_path = ROOT / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def read_brand(brand: str) -> str:
    folder = BRANDS / brand
    if not folder.is_dir():
        raise SystemExit(f"Unknown brand folder: {folder}")
    parts = []
    for name in ("voice-samples.md", "products-services.md", "audience.md", "README.md"):
        p = folder / name
        if p.exists():
            parts.append(f"## {name}\n{p.read_text().strip()}\n")
    if not parts:
        raise SystemExit(f"No brand context files in {folder}")
    return "\n".join(parts)


def slugify(text: str) -> str:
    s = text.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s[:80] or "article"


def ollama_generate(prompt: str, model: str, host: str) -> str:
    url = f"{host.rstrip('/')}/api/generate"
    payload = {"model": model, "prompt": prompt, "stream": False}
    r = requests.post(url, json=payload, timeout=300)
    r.raise_for_status()
    data = r.json()
    return data.get("response", "").strip()


def build_prompt(brand: str, topic: str, keyword: str, brand_ctx: str) -> str:
    return f"""You are a careful SEO/GEO content writer for a personal business site.
Write one complete article in Markdown only (no preamble).

Brand key: {brand}
Primary keyword / topic: {keyword or topic}
Article angle / topic: {topic}

Brand context (follow voice and facts; do not invent products or prices not implied here):
{brand_ctx}

Requirements:
1. Start with YAML front-matter between --- lines containing:
   title, slug, brand, keyword, meta_description (max 155 chars), date ({date.today().isoformat()}), status: draft
2. H1 matching title
3. 900–1400 words, scannable H2/H3 structure
4. Natural use of the primary keyword in title, first paragraph, one H2, and conclusion
5. Practical, accurate guidance; no medical/legal guarantees
6. End with a short FAQ (3 questions) and a soft CTA aligned with the brand
7. Suggest 2–3 internal link placeholders like [[link: relevant-page]]
8. No fabricated statistics; if citing trends keep them qualitative

Output Markdown only."""


def append_log(row: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    if not LOG.exists():
        LOG.write_text(
            "# Article Log\n\n| Date | Brand | Title | Keyword | Status | Notes |\n"
            "|------|-------|-------|---------|--------|-------|\n"
        )
    with LOG.open("a") as f:
        f.write(row + "\n")


def main() -> None:
    load_env()
    parser = argparse.ArgumentParser(description="Generate SEO article via Ollama")
    parser.add_argument("--brand", required=True, choices=["mynailstudio", "caebikes"])
    parser.add_argument("--topic", required=True, help="Article topic / angle")
    parser.add_argument("--keyword", default="", help="Primary SEO keyword")
    parser.add_argument("--model", default=os.getenv("OLLAMA_MODEL", "llama3.1:8b"))
    parser.add_argument("--host", default=os.getenv("OLLAMA_HOST", "http://localhost:11434"))
    parser.add_argument("--dry-run", action="store_true", help="Print prompt only")
    args = parser.parse_args()

    brand_ctx = read_brand(args.brand)
    prompt = build_prompt(args.brand, args.topic, args.keyword or args.topic, brand_ctx)

    if args.dry_run:
        print(prompt)
        return

    print(f"Generating with Ollama model={args.model} ...", file=sys.stderr)
    try:
        body = ollama_generate(prompt, args.model, args.host)
    except requests.RequestException as e:
        print(f"Ollama error: {e}\nIs Ollama running? Try: ollama serve && ollama pull {args.model}", file=sys.stderr)
        sys.exit(1)

    # Ensure front-matter exists; if model skipped it, wrap lightly
    if not body.startswith("---"):
        title = args.topic.strip()
        slug = slugify(title)
        fm = (
            f"---\ntitle: \"{title}\"\nslug: {slug}\nbrand: {args.brand}\n"
            f"keyword: {args.keyword or args.topic}\nmeta_description: {title[:150]}\n"
            f"date: {date.today().isoformat()}\nstatus: draft\n---\n\n"
        )
        body = fm + body

    out_dir = ARTICLES / args.brand
    out_dir.mkdir(parents=True, exist_ok=True)
    # Prefer slug from front-matter
    m = re.search(r"^slug:\s*[\"']?([\w-]+)", body, re.M)
    slug = m.group(1) if m else slugify(args.topic)
    out_path = out_dir / f"{date.today().isoformat()}-{slug}.md"
    out_path.write_text(body if body.endswith("\n") else body + "\n")
    print(str(out_path))

    title_m = re.search(r"^title:\s*[\"']?([^\"'\n]+)", body, re.M)
    title = title_m.group(1).strip() if title_m else args.topic
    append_log(
        f"| {date.today().isoformat()} | {args.brand} | {title} | {args.keyword or args.topic} | draft | {out_path.name} |"
    )


if __name__ == "__main__":
    main()
