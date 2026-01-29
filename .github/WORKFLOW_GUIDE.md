# GitHub Action Configuration Guide

## Updating Your RSS Feed URL

The GitHub Action workflow is configured to fetch blog posts from RSS feeds. To use your own blog feed:

### Step 1: Find Your RSS Feed URL

Common RSS feed formats:
- **Dev.to**: `https://dev.to/feed/YOUR_USERNAME`
- **Medium**: `https://medium.com/feed/@YOUR_USERNAME`
- **Hashnode**: `https://YOUR_USERNAME.hashnode.dev/rss.xml`
- **WordPress**: `https://YOUR_SITE.com/feed/`
- **Ghost**: `https://YOUR_SITE.com/rss/`
- **Substack**: `https://YOUR_NEWSLETTER.substack.com/feed`

### Step 2: Update the Workflow File

1. Open `.github/workflows/update-blog-json.yml`
2. Find the line with `feed_list:` (around line 39)
3. Replace the example URL with your actual RSS feed URL(s)
4. You can add multiple feeds separated by commas:
   ```yaml
   feed_list: "https://dev.to/feed/yourusername,https://medium.com/feed/@yourusername"
   ```

### Step 3: Customize Blog Post Count (Optional)

To change the maximum number of blog posts fetched:
1. Find the line with `max_post_count:` (around line 41)
2. Change the value (default is 10):
   ```yaml
   max_post_count: 20
   ```

### Step 4: Enable Workflow Permissions

For the workflow to push changes to your repository:

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Scroll down to **Workflow permissions**
4. Select **Read and write permissions**
5. Click **Save**

### Step 5: Test the Workflow

#### Manual Test:
1. Go to **Actions** tab in your repository
2. Click on **Update Blog JSON Daily** workflow
3. Click **Run workflow** button
4. Select the branch and click **Run workflow**
5. Wait for the workflow to complete
6. Check the `blogs.json` file for updates

#### Automatic Updates:
- The workflow runs automatically every day at 00:00 UTC
- New blog posts from your RSS feed will be automatically added to `blogs.json`
- The existing JSON structure will be preserved

## How It Works

1. **Fetch**: The workflow fetches the latest posts from your RSS feed using the `blog-post-workflow` action
2. **Convert**: A Node.js script converts the RSS data to match your `blogs.json` structure
3. **Merge**: New posts are added to the beginning of the blogs array
4. **Deduplicate**: Posts with the same title are not added again
5. **Commit**: If there are changes, they are automatically committed and pushed

## Troubleshooting

### No posts are being added
- Verify your RSS feed URL is correct by opening it in a browser
- Check the workflow logs in the Actions tab for errors
- Ensure the RSS feed contains valid posts with titles and URLs

### Workflow permissions error
- Make sure you've enabled "Read and write permissions" in repository settings
- See Step 4 above for instructions

### JSON structure changed
- The workflow preserves your existing JSON structure
- New posts are added with fields matching the existing format
- Categories and settings are never modified

## Customization

### Change Author Information
Edit line ~112 in `.github/workflows/update-blog-json.yml`:
```javascript
author: {
  name: "Your Name",
  avatar: "/images/your-avatar.jpg",
  bio: "Your Bio"
}
```

### Change Default Category
Edit line ~122 in `.github/workflows/update-blog-json.yml`:
```javascript
category: "Your Default Category"
```

### Change Schedule
Edit lines 4-6 in `.github/workflows/update-blog-json.yml`:
```yaml
schedule:
  - cron: '0 */12 * * *'  # Run every 12 hours
```

Common cron schedules:
- Every hour: `'0 * * * *'`
- Every 6 hours: `'0 */6 * * *'`
- Every day at noon: `'0 12 * * *'`
- Every week: `'0 0 * * 0'`
