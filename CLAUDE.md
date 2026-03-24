# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Purpose

This repository is a centralized data store for a portfolio website. It contains:
- `portfolio.json` — personal info, experience, skills, and projects
- `blogs.json` — curated blog posts aggregated from RSS feeds
- A Python-based RSS processor
- A GitHub Actions workflow that auto-updates `blogs.json` daily

## Common Commands

```bash
# Run the full test suite
python3 test_rss_processor.py

# Run the RSS processor in dry-run mode (preview without writing)
python3 rss_feed_processor.py test_rss_feed.xml

# Run the RSS processor and update blogs.json
python3 rss_feed_processor.py test_rss_feed.xml --update

# Run the integration demo
python3 demo_integration.py

# Validate RSS feed URLs
bash test_new_feeds.sh

# Manually trigger the GitHub Actions workflow
gh workflow run update-blog-json.yml
```

## Architecture

### Data Flow

```
RSS Feeds (10+ sources)
    ↓
GitHub Actions Workflow (.github/workflows/update-blog-json.yml)
  Runs daily at 00:00 UTC, or on manual dispatch
    ↓
Node.js inline script (fetches feeds, deduplicates, merges)
    ↓
blogs.json (committed back to repo)
    ↓
Portfolio website consumes portfolio.json + blogs.json
```

### Key Components

**`rss_feed_processor.py`** — Core Python processor (stdlib only, no pip installs needed). Key functions:
- `parse_rss_feed(xml_content)` — parses RSS XML into normalized blog entries
- `merge_blogs(existing, new)` — merges with duplicate detection (by title + URL)
- Handles categorization, SEO metadata, slug generation, and excerpt extraction

**`.github/workflows/update-blog-json.yml`** — Automated workflow. Uses Node.js 20 to fetch and process feeds. Commits changes back to `main` only if `blogs.json` changed.

**`.claude/agents/`** — Five specialized Claude agents for RSS and blog automation tasks. Use these via the `Agent` tool for delegated tasks:
- `rss-feed-parser` — fetch and normalize RSS feeds
- `rss-blog-transformer` — convert RSS entries to `blogs.json` schema
- `rss-feed-curator` — discover and score quality RSS sources
- `blog-merge-dedup` — safely merge entries into `blogs.json`
- `github-action-orchestrator` — create/configure GitHub Actions workflows

### Data Schemas

**`blogs.json`** structure:
```json
{
  "blogs": [
    {
      "id": 1,
      "slug": "url-friendly-slug",
      "title": "...",
      "description": "...",
      "excerpt": "150-200 char summary",
      "author": "...",
      "publishDate": "YYYY-MM-DD",
      "lastModified": "YYYY-MM-DD",
      "readTime": "5 min read",
      "category": "Technology|AI|Startups|Security",
      "tags": ["..."],
      "image": "url",
      "featured": false,
      "views": 0,
      "seo": { "metaTitle": "...", "metaDescription": "...", "keywords": [], "ogImage": "...", "canonicalUrl": "..." },
      "externalUrl": "original_source_url"
    }
  ]
}
```

**`portfolio.json`** top-level keys: `personal`, `social`, `experience`, `skills`, `projects`.

### Deduplication Logic

Entries in `blogs.json` are deduplicated by both title (case-insensitive) and `externalUrl`. The `blog-merge-dedup` agent also checks slugs and content hashes.

### RSS Feed Sources

Configured in `.github/workflows/update-blog-json.yml`. Current sources include Stack Overflow Blog, FreeCodeCamp, Dev.to, ML Mastery, MIT AI News, Smashing Magazine, Hacker News, Ars Technica, The Verge, and Artificial Intelligence News.
