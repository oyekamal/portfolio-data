# portfolio-data

This repository contains portfolio and blog data in JSON format that is automatically updated daily.

## Automated Blog Updates

This repository includes a GitHub Action workflow that automatically updates the `blogs.json` file with the latest blog posts from your RSS feed every day at 00:00 UTC.

### How It Works

1. **Daily Schedule**: The workflow runs automatically once per day
2. **RSS Feed Fetching**: Fetches latest posts from configured RSS feed(s)
3. **JSON Update**: Converts RSS feed data to JSON and adds new posts to `blogs.json`
4. **Structure Preservation**: Maintains the existing JSON structure without disrupting current data
5. **Automatic Commit**: Commits and pushes changes back to the repository

### Configuration

To configure your own RSS feed(s), edit `.github/workflows/update-blog-json.yml` and update the `feed_list` parameter:

```yaml
feed_list: "https://dev.to/feed/yourusername,https://medium.com/feed/@yourusername"
```

### Supported RSS Feed Sources

- Dev.to: `https://dev.to/feed/username`
- Medium: `https://medium.com/feed/@username`
- Hashnode: `https://username.hashnode.dev/rss.xml`
- WordPress: `https://yourblog.com/feed/`
- Ghost: `https://yourblog.com/rss/`

### Manual Trigger

You can manually trigger the workflow at any time:
1. Go to the "Actions" tab in your repository
2. Select "Update Blog JSON Daily" workflow
3. Click "Run workflow"

### Files

- `blogs.json` - Contains all blog posts with full content and metadata
- `portfolio.json` - Contains portfolio information
- `.github/workflows/update-blog-json.yml` - Automated blog update workflow
