#!/usr/bin/env python3
"""
RSS Feed Processor for Portfolio Data
Fetches TechCrunch RSS feed and transforms it to blogs.json format
"""

import json
import xml.etree.ElementTree as ET
from datetime import datetime
from typing import List, Dict, Any
import re


def parse_rss_feed(xml_content: str) -> List[Dict[str, Any]]:
    """
    Parse RSS feed XML content and extract blog data
    
    Args:
        xml_content: Raw RSS XML content as string
        
    Returns:
        List of blog entries in portfolio format
    """
    try:
        root = ET.fromstring(xml_content)
        items = root.findall('.//item')
        
        blogs = []
        for idx, item in enumerate(items, start=1):
            # Extract basic fields from RSS
            title = item.find('title')
            link = item.find('link')
            description = item.find('description')
            pub_date = item.find('pubDate')
            creator = item.find('{http://purl.org/dc/elements/1.1/}creator')
            
            # Get categories/tags
            categories = [cat.text for cat in item.findall('category') if cat.text]
            
            # Parse publication date
            publish_date = ""
            if pub_date is not None and pub_date.text:
                try:
                    # Parse RFC 822 format: "Wed, 29 Jan 2025 09:00:00 +0000"
                    dt = datetime.strptime(pub_date.text[:25], '%a, %d %b %Y %H:%M:%S')
                    publish_date = dt.strftime('%Y-%m-%d')
                except (ValueError, IndexError):
                    publish_date = datetime.now().strftime('%Y-%m-%d')
            
            # Clean HTML from description
            desc_text = description.text if description is not None else ""
            clean_desc = re.sub(r'<[^>]+>', '', desc_text)
            clean_desc = clean_desc.strip()[:500] if clean_desc else ""
            
            # Create slug from title
            title_text = title.text if title is not None else f"article-{idx}"
            slug = re.sub(r'[^\w\s-]', '', title_text.lower())
            slug = re.sub(r'[-\s]+', '-', slug)[:100]
            
            # Determine category from tags
            category = "Technology"
            if categories:
                if any(cat.lower() in ['startup', 'startups'] for cat in categories):
                    category = "Startups"
                elif any(cat.lower() in ['ai', 'artificial intelligence', 'machine learning'] for cat in categories):
                    category = "Artificial Intelligence"
                elif any(cat.lower() in ['security', 'cybersecurity'] for cat in categories):
                    category = "Security"
            
            # Create excerpt (max 200 chars including ellipsis)
            if len(clean_desc) > 197:
                excerpt = clean_desc[:197] + "..."
            else:
                excerpt = clean_desc
            
            # Build blog entry with temporary ID (will be assigned during merge)
            blog_entry = {
                "id": 0,  # Temporary ID, will be assigned during merge
                "slug": slug,
                "title": title_text,
                "description": clean_desc,
                "content": clean_desc,
                "excerpt": excerpt,
                "author": creator.text if creator is not None else "TechCrunch",
                "publishDate": publish_date,
                "lastModified": publish_date,
                "readTime": "5 min read",
                "category": category,
                "tags": categories[:7] if categories else ["Technology"],
                "image": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=800&q=80",
                "featured": idx <= 2,  # First 2 are featured
                "views": 0,
                "seo": {
                    "metaTitle": f"{title_text} | TechCrunch",
                    "metaDescription": clean_desc[:160],
                    "keywords": categories[:10] if categories else ["technology", "techcrunch"],
                    "ogImage": "https://images.unsplash.com/photo-1488590528505-98d2b5aba04b?w=1200&q=80",
                    "canonicalUrl": link.text if link is not None else ""
                }
            }
            
            blogs.append(blog_entry)
        
        return blogs
    
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse RSS feed: {e}")


def merge_blogs(existing_blogs: List[Dict], new_blogs: List[Dict], max_entries: int = 10) -> List[Dict]:
    """
    Merge new blog entries with existing ones
    
    Args:
        existing_blogs: Current blog entries
        new_blogs: New blog entries from RSS feed
        max_entries: Maximum number of total entries to keep
        
    Returns:
        Merged list of blog entries
    """
    # Update IDs to avoid conflicts
    if existing_blogs:
        max_id = max(blog['id'] for blog in existing_blogs)
        for idx, blog in enumerate(new_blogs, start=1):
            blog['id'] = max_id + idx
    
    # Combine and limit
    all_blogs = new_blogs + existing_blogs
    return all_blogs[:max_entries]


def load_blogs_json(filepath: str) -> Dict[str, Any]:
    """Load blogs.json file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_blogs_json(filepath: str, data: Dict[str, Any]) -> None:
    """Save blogs.json file with proper formatting"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def process_rss_feed(rss_content: str, blogs_json_path: str, update_file: bool = False) -> List[Dict]:
    """
    Main function to process RSS feed and optionally update blogs.json
    
    Args:
        rss_content: Raw RSS XML content
        blogs_json_path: Path to blogs.json file
        update_file: Whether to update the blogs.json file
        
    Returns:
        List of processed blog entries
    """
    # Parse RSS feed
    new_blogs = parse_rss_feed(rss_content)
    
    if update_file:
        # Load existing blogs.json
        blogs_data = load_blogs_json(blogs_json_path)
        
        # Merge blogs
        blogs_data['blogs'] = merge_blogs(blogs_data['blogs'], new_blogs)
        
        # Save updated file
        save_blogs_json(blogs_json_path, blogs_data)
    
    return new_blogs


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 rss_feed_processor.py <rss_file_path> [--update]")
        print("  rss_file_path: Path to RSS XML file")
        print("  --update: Optional flag to update blogs.json")
        sys.exit(1)
    
    rss_file = sys.argv[1]
    update = '--update' in sys.argv
    
    # Read RSS content
    with open(rss_file, 'r', encoding='utf-8') as f:
        rss_content = f.read()
    
    # Process feed
    blogs_json_path = 'blogs.json'
    blogs = process_rss_feed(rss_content, blogs_json_path, update_file=update)
    
    print(f"Processed {len(blogs)} blog entries from RSS feed")
    if update:
        print(f"Updated {blogs_json_path}")
    else:
        print("Dry run - no files updated")
        print("\nFirst entry:")
        print(json.dumps(blogs[0], indent=2))
