# GitHub Action Workflow - Blog JSON Updater

## Workflow Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Daily at 00:00 UTC                           │
│                    (or Manual Trigger)                          │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: Checkout Repository                                    │
│  - Fetches latest code from GitHub                              │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: Setup Node.js Environment                              │
│  - Installs Node.js v20 for running scripts                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: Fetch RSS Feed                                         │
│  - Uses gautamkrishnar/blog-post-workflow action                │
│  - Reads your configured RSS feed URL(s)                        │
│  - Generates markdown with blog post links                      │
│  - Output: /tmp/temp_readme.md                                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: Process Blog Posts                                     │
│  - Parses markdown to extract titles and URLs                   │
│  - Reads existing blogs.json                                    │
│  - Checks for duplicates (by title and URL)                     │
│  - Creates new blog entries with proper structure               │
│  - Generates unique IDs (max existing ID + 1)                   │
│  - Adds posts to beginning of blogs array                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: Check for Changes                                      │
│  - Uses git diff to detect modifications                        │
│  - Sets output flag if blogs.json changed                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
                  ┌─────────┴──────────┐
                  │  Changes detected? │
                  └─────────┬──────────┘
                            │
               ┌────────────┼────────────┐
               │ No         │         Yes│
               ▼            ▼            ▼
         ┌─────────┐  ┌──────────────────────┐
         │  Skip   │  │  Step 6: Commit      │
         │ Commit  │  │  - Stage blogs.json  │
         └────┬────┘  │  - Create commit     │
              │       │  - Push to GitHub    │
              │       └──────────┬───────────┘
              │                  │
              └────────┬─────────┘
                       │
                       ▼
         ┌─────────────────────────┐
         │  Step 7: Summary        │
         │  - Display statistics   │
         │  - Show blog count      │
         └─────────────────────────┘
```

## Blog Entry Structure

When a new blog post is found in your RSS feed, it's converted to this structure:

```json
{
  "id": <unique ID>,
  "slug": "post-title-slugified",
  "title": "Post Title from RSS Feed",
  "description": "Imported from RSS feed: Post Title",
  "content": {
    "introduction": "This post was imported from an external blog...",
    "sections": [],
    "conclusion": "",
    "keyTakeaways": []
  },
  "excerpt": "Post Title",
  "author": "Muhammad Kamal",
  "publishDate": "2026-01-29",
  "lastModified": "2026-01-29",
  "readTime": "5 min read",
  "category": "Technology",
  "tags": ["External", "Blog"],
  "image": "https://images.unsplash.com/...",
  "featured": false,
  "views": 0,
  "seo": {
    "metaTitle": "Post Title",
    "metaDescription": "Post Title",
    "keywords": ["blog", "external"],
    "ogImage": "https://images.unsplash.com/...",
    "canonicalUrl": "https://your-blog.com/original-post"
  },
  "externalUrl": "https://your-blog.com/original-post"
}
```

## Duplicate Prevention

The workflow prevents duplicates using two checks:

1. **Title Check**: Compares post title with existing blog titles
2. **URL Check**: Compares post URL with existing `externalUrl` fields

A post is only added if BOTH title AND URL are new.

## Customization Points

### 1. RSS Feed URL
```yaml
feed_list: "https://dev.to/feed/yourusername"
```

### 2. Max Posts to Fetch
```yaml
max_post_count: 10
```

### 3. Schedule
```yaml
cron: '0 0 * * *'  # Daily at midnight UTC
```

### 4. Author Name
```javascript
author: "Muhammad Kamal"  # Change in the Node.js script
```

### 5. Default Category
```javascript
category: "Technology"  # Change in the Node.js script
```

### 6. Default Image
```javascript
image: "https://images.unsplash.com/..."  # Change in the Node.js script
```

## Supported RSS Feed Sources

| Platform | RSS Feed URL Format |
|----------|---------------------|
| Dev.to | `https://dev.to/feed/username` |
| Medium | `https://medium.com/feed/@username` |
| Hashnode | `https://username.hashnode.dev/rss.xml` |
| WordPress | `https://yourblog.com/feed/` |
| Ghost | `https://yourblog.com/rss/` |
| Substack | `https://newsletter.substack.com/feed` |

## Troubleshooting

### Workflow doesn't run
- Check workflow permissions are set to "Read and write"
- Verify RSS feed URL is valid
- Check Actions tab for error messages

### No posts are added
- Verify RSS feed has new posts
- Check if posts already exist (duplicate detection)
- Review workflow logs for errors

### JSON structure is invalid
- The workflow matches the exact structure of your blogs.json
- If you modify blogs.json structure, update the Node.js script accordingly

## Safety Features

✅ **Never modifies existing posts** - Only adds new entries  
✅ **Preserves categories** - Categories array untouched  
✅ **Preserves settings** - Settings object untouched  
✅ **Validates before commit** - Only commits if changes detected  
✅ **Unique IDs** - Generates IDs based on max existing ID  
✅ **Duplicate prevention** - Checks both title and URL  

## Performance

- **Runtime**: ~30-60 seconds per execution
- **API Calls**: Minimal (only RSS feed fetch)
- **Cost**: Free (within GitHub Actions limits)
- **Frequency**: Daily (customizable)

## Security

✅ No secrets required (uses built-in GitHub token)  
✅ Read-only RSS feed access  
✅ No external code execution  
✅ CodeQL verified (no vulnerabilities)  
✅ Minimal permissions (only needs contents: write)  
