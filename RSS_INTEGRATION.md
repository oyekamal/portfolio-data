# RSS Feed Integration

This directory contains tools for integrating TechCrunch RSS feeds into the portfolio blog data.

## Files

- `rss_feed_processor.py` - Main script to fetch and process RSS feeds
- `test_rss_feed.xml` - Sample TechCrunch RSS feed for testing
- `test_rss_processor.py` - Comprehensive test suite
- `blogs.json` - Blog data in portfolio format

## Features

The RSS feed processor provides:

1. **RSS Feed Parsing**: Parses RSS XML and extracts blog entries
2. **Data Transformation**: Converts RSS items to portfolio blog format
3. **Intelligent Categorization**: Automatically categorizes blogs based on tags
4. **SEO Optimization**: Generates SEO metadata for each blog entry
5. **Blog Merging**: Merges new RSS entries with existing blogs
6. **Comprehensive Testing**: Full test suite to validate functionality

## Usage

### Running Tests

To test the RSS feed integration:

```bash
python3 test_rss_processor.py
```

This will run all tests including:
- RSS XML structure validation
- Blog data parsing
- Data quality checks
- Blog merging functionality
- Full integration testing

### Processing RSS Feed

To process an RSS feed without updating blogs.json (dry run):

```bash
python3 rss_feed_processor.py test_rss_feed.xml
```

To process and update blogs.json:

```bash
python3 rss_feed_processor.py test_rss_feed.xml --update
```

### Using with Real TechCrunch Feed

1. Download the TechCrunch RSS feed:
   ```bash
   curl -o techcrunch_feed.xml https://techcrunch.com/feed/
   ```

2. Process the feed:
   ```bash
   python3 rss_feed_processor.py techcrunch_feed.xml --update
   ```

## Blog Entry Format

Each blog entry in `blogs.json` contains:

```json
{
  "id": 1,
  "slug": "article-slug",
  "title": "Article Title",
  "description": "Full description",
  "content": "Article content",
  "excerpt": "Short excerpt",
  "author": "Author Name",
  "publishDate": "2026-01-29",
  "lastModified": "2026-01-29",
  "readTime": "5 min read",
  "category": "Technology",
  "tags": ["tag1", "tag2"],
  "image": "https://...",
  "featured": false,
  "views": 0,
  "seo": {
    "metaTitle": "...",
    "metaDescription": "...",
    "keywords": ["..."],
    "ogImage": "...",
    "canonicalUrl": "..."
  }
}
```

## Automatic Categorization

The processor automatically categorizes articles based on their tags:

- **Startups**: Articles tagged with "startup" or "startups"
- **Artificial Intelligence**: Articles with "ai", "artificial intelligence", or "machine learning"
- **Security**: Articles tagged with "security" or "cybersecurity"
- **Technology**: Default category for other articles

## Test Coverage

The test suite validates:

✓ RSS feed XML structure  
✓ Parsing of all blog fields  
✓ Data quality and format  
✓ Date format (YYYY-MM-DD)  
✓ SEO metadata generation  
✓ Blog merging with ID management  
✓ Full integration with blogs.json  

## Requirements

- Python 3.7+
- Standard library only (no external dependencies required)

## Example Output

When processing the test RSS feed:

```
Processed 8 blog entries from RSS feed
Updated blogs.json

First entry:
{
  "id": 1,
  "slug": "ai-startup-raises-100m-series-b-to-transform-healthcare",
  "title": "AI Startup Raises $100M Series B to Transform Healthcare",
  ...
}
```

## Notes

- The processor preserves existing blog entries when updating
- New entries are added at the beginning of the blog list
- IDs are automatically managed to avoid conflicts
- All HTML tags are stripped from descriptions
- SEO descriptions are limited to 160 characters
- First 2 entries are automatically marked as featured
