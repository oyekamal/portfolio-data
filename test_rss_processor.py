#!/usr/bin/env python3
"""
Test script for RSS feed processor
Tests the TechCrunch RSS feed integration
"""

import json
import sys
import os
from typing import Dict, Any
import xml.etree.ElementTree as ET

# Import the RSS processor
from rss_feed_processor import parse_rss_feed, merge_blogs, process_rss_feed


def test_parse_rss_feed():
    """Test parsing RSS feed XML"""
    print("\n=== Testing RSS Feed Parsing ===")
    
    # Read test RSS feed
    with open('test_rss_feed.xml', 'r', encoding='utf-8') as f:
        rss_content = f.read()
    
    # Parse feed
    blogs = parse_rss_feed(rss_content)
    
    # Assertions
    assert len(blogs) > 0, "Should parse at least one blog entry"
    assert isinstance(blogs, list), "Should return a list"
    
    # Check first blog structure
    first_blog = blogs[0]
    required_fields = ['id', 'slug', 'title', 'description', 'content', 'excerpt', 
                      'author', 'publishDate', 'readTime', 'category', 'tags', 
                      'image', 'featured', 'views', 'seo']
    
    for field in required_fields:
        assert field in first_blog, f"Blog should have '{field}' field"
    
    # Check SEO structure
    seo_fields = ['metaTitle', 'metaDescription', 'keywords', 'ogImage', 'canonicalUrl']
    for field in seo_fields:
        assert field in first_blog['seo'], f"SEO should have '{field}' field"
    
    print(f"✓ Successfully parsed {len(blogs)} blog entries")
    print(f"✓ First blog title: {first_blog['title']}")
    print(f"✓ First blog author: {first_blog['author']}")
    print(f"✓ First blog category: {first_blog['category']}")
    print(f"✓ First blog tags: {', '.join(first_blog['tags'])}")
    
    return blogs


def test_blog_data_quality(blogs):
    """Test the quality of parsed blog data"""
    print("\n=== Testing Blog Data Quality ===")
    
    for idx, blog in enumerate(blogs):
        # Check required string fields are not empty
        assert blog['title'], f"Blog {idx} should have non-empty title"
        assert blog['slug'], f"Blog {idx} should have non-empty slug"
        assert blog['description'], f"Blog {idx} should have non-empty description"
        assert blog['author'], f"Blog {idx} should have non-empty author"
        assert blog['publishDate'], f"Blog {idx} should have non-empty publishDate"
        
        # Check date format (YYYY-MM-DD)
        assert len(blog['publishDate']) == 10, f"Blog {idx} date should be in YYYY-MM-DD format"
        assert blog['publishDate'].count('-') == 2, f"Blog {idx} date should have 2 hyphens"
        
        # Check tags is a list
        assert isinstance(blog['tags'], list), f"Blog {idx} tags should be a list"
        assert len(blog['tags']) > 0, f"Blog {idx} should have at least one tag"
        
        # Check featured is boolean
        assert isinstance(blog['featured'], bool), f"Blog {idx} featured should be boolean"
        
        # Check views is integer
        assert isinstance(blog['views'], int), f"Blog {idx} views should be integer"
        
        # Check SEO fields
        assert blog['seo']['metaTitle'], f"Blog {idx} should have SEO metaTitle"
        assert blog['seo']['metaDescription'], f"Blog {idx} should have SEO metaDescription"
        assert len(blog['seo']['metaDescription']) <= 160, f"Blog {idx} meta description should be <= 160 chars"
        
    print(f"✓ All {len(blogs)} blogs have valid data structure")
    print(f"✓ All required fields are present and non-empty")
    print(f"✓ Date formats are correct")
    print(f"✓ SEO metadata is properly formatted")


def test_merge_blogs(new_blogs):
    """Test merging new blogs with existing ones"""
    print("\n=== Testing Blog Merging ===")
    
    # Create mock existing blogs
    existing_blogs = [
        {"id": 1, "title": "Existing Blog 1", "slug": "existing-1"},
        {"id": 2, "title": "Existing Blog 2", "slug": "existing-2"}
    ]
    
    # Merge
    merged = merge_blogs(existing_blogs, new_blogs[:3], max_entries=5)
    
    # Assertions
    assert len(merged) == 5, "Should limit to max_entries"
    assert merged[0]['id'] > 2, "New blogs should have IDs higher than existing"
    assert merged[3]['id'] == 1, "Existing blogs should be at the end"
    
    print(f"✓ Successfully merged blogs")
    print(f"✓ New blog IDs start at {merged[0]['id']}")
    print(f"✓ Limited to {len(merged)} entries as specified")


def test_process_full_integration():
    """Test full integration with blogs.json"""
    print("\n=== Testing Full Integration ===")
    
    # Read RSS content
    with open('test_rss_feed.xml', 'r', encoding='utf-8') as f:
        rss_content = f.read()
    
    # Create backup of blogs.json
    import shutil
    if os.path.exists('blogs.json'):
        shutil.copy('blogs.json', 'blogs.json.backup')
    
    try:
        # Process feed with update
        blogs = process_rss_feed(rss_content, 'blogs.json', update_file=True)
        
        # Verify blogs.json was updated
        with open('blogs.json', 'r', encoding='utf-8') as f:
            blogs_data = json.load(f)
        
        assert 'blogs' in blogs_data, "blogs.json should have 'blogs' key"
        assert len(blogs_data['blogs']) > 0, "Should have at least one blog"
        
        # Check that new blogs are at the beginning
        first_blog = blogs_data['blogs'][0]
        # Verify first blog is from RSS feed (has author and 2026 date)
        assert first_blog.get('publishDate', '').startswith('2026'), \
            "First blog should be from the 2026 RSS feed"
        
        print(f"✓ Successfully integrated RSS feed into blogs.json")
        print(f"✓ Total blogs in blogs.json: {len(blogs_data['blogs'])}")
        print(f"✓ First blog: {first_blog['title']}")
        
    finally:
        # Restore backup
        if os.path.exists('blogs.json.backup'):
            shutil.move('blogs.json.backup', 'blogs.json')
            print("✓ Restored original blogs.json")


def test_rss_feed_structure():
    """Test the RSS feed XML structure"""
    print("\n=== Testing RSS Feed XML Structure ===")
    
    with open('test_rss_feed.xml', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse XML
    root = ET.fromstring(content)
    
    # Check structure
    assert root.tag == 'rss', "Root should be 'rss'"
    channel = root.find('channel')
    assert channel is not None, "Should have 'channel' element"
    
    items = root.findall('.//item')
    assert len(items) > 0, "Should have at least one item"
    
    # Check first item has required fields
    first_item = items[0]
    assert first_item.find('title') is not None, "Item should have title"
    assert first_item.find('link') is not None, "Item should have link"
    assert first_item.find('description') is not None, "Item should have description"
    assert first_item.find('pubDate') is not None, "Item should have pubDate"
    
    print(f"✓ RSS feed XML is well-formed")
    print(f"✓ Contains {len(items)} items")
    print(f"✓ All required fields are present")


def print_sample_blog(blogs):
    """Print a sample blog entry for inspection"""
    print("\n=== Sample Blog Entry ===")
    if blogs:
        print(json.dumps(blogs[0], indent=2))


def main():
    """Run all tests"""
    print("=" * 60)
    print("RSS Feed Processor Test Suite")
    print("=" * 60)
    
    try:
        # Run tests
        test_rss_feed_structure()
        blogs = test_parse_rss_feed()
        test_blog_data_quality(blogs)
        test_merge_blogs(blogs)
        test_process_full_integration()
        print_sample_blog(blogs)
        
        print("\n" + "=" * 60)
        print("✓ ALL TESTS PASSED!")
        print("=" * 60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
