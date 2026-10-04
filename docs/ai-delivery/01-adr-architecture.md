# ADR: Local-first CLI + Markdown Pipeline

**Status:** Approved  
**Date:** 2026-09-30

## Decision
Use a local-first CLI + Markdown pipeline (Option A).

Primary model: Ollama (model that runs on operator hardware).  
Optional free-cloud fallbacks for overflow.  
Articles stored as Markdown with front-matter.  
Shopify publishes as draft only.  
Base44 content is staged for manual insertion or GitHub sync.

## Rationale
- Zero recurring cost  
- Highest privacy  
- Smallest attack surface  
- Easy human review and rollback  
- Matches personal-use constraint

## Alternatives rejected
- Full local web app (unnecessary complexity)  
- Fully cloud free-tier (privacy + rate-limit risk)
