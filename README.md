# portfolio-data

This repository contains portfolio and blog data in JSON format that is automatically updated daily.

## Automated Blog Updates

This repository includes a GitHub Action workflow that automatically updates the `blogs.json` file with the latest blog posts from your RSS feed every day at 00:00 UTC.

### ⚠️ Configuration Required

**The workflow is currently using a placeholder RSS feed URL and needs to be configured before it will work.**

To enable automatic blog updates:

1. **Find your RSS feed URL** from one of the supported platforms:
   - **Dev.to**: `https://dev.to/feed/yourusername`
   - **Medium**: `https://medium.com/feed/@yourusername`
   - **Hashnode**: `https://yourusername.hashnode.dev/rss.xml`
   - **WordPress**: `https://yourblog.com/feed/`
   - **Ghost**: `https://yourblog.com/rss/`
   - **Substack**: `https://yournewsletter.substack.com/feed`

2. **Update the workflow file**: Edit `.github/workflows/update-blog-json.yml`
   - Find the `feed_list` parameter (around line 67)
   - Replace the placeholder with your actual RSS feed URL(s)
   - You can add multiple feeds separated by commas:
     ```yaml
     feed_list: "https://dev.to/feed/yourusername,https://medium.com/feed/@yourusername"
     ```

3. **Enable workflow permissions**:
   - Go to your repository on GitHub
   - Navigate to **Settings** → **Actions** → **General**
   - Under **Workflow permissions**, select **Read and write permissions**
   - Click **Save**

### How It Works

1. **Daily Schedule**: The workflow runs automatically once per day
2. **RSS Feed Fetching**: Fetches latest posts from configured RSS feed(s)
3. **JSON Update**: Converts RSS feed data to JSON and adds new posts to `blogs.json`
4. **Structure Preservation**: Maintains the existing JSON structure without disrupting current data
5. **Automatic Commit**: Commits and pushes changes back to the repository

### Configuration

**Before the workflow can work, you must configure your RSS feed URL.**

To configure your own RSS feed(s), edit `.github/workflows/update-blog-json.yml` and update the `feed_list` parameter:

```yaml
feed_list: "https://dev.to/feed/yourusername,https://medium.com/feed/@yourusername"
```

For detailed setup instructions, see [Workflow Configuration Guide](.github/WORKFLOW_GUIDE.md).

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
