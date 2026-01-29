#!/usr/bin/env python3
"""
Demo script showing TechCrunch RSS integration
This demonstrates how the RSS feed processor works end-to-end
"""

import json
import shutil
from rss_feed_processor import process_rss_feed

print("=" * 70)
print("TechCrunch RSS Feed Integration Demo")
print("=" * 70)

# Step 1: Show original blogs
print("\n1. Loading original blogs.json...")
with open('blogs.json', 'r') as f:
    original = json.load(f)
    original_count = len(original['blogs'])
    print(f"   ✓ Original blog count: {original_count}")
    print(f"   ✓ First blog: {original['blogs'][0]['title']}")

# Step 2: Read RSS feed
print("\n2. Reading TechCrunch RSS feed (test_rss_feed.xml)...")
with open('test_rss_feed.xml', 'r') as f:
    rss_content = f.read()
    print(f"   ✓ RSS feed loaded successfully")

# Step 3: Parse RSS feed
print("\n3. Parsing RSS feed entries...")
from rss_feed_processor import parse_rss_feed
new_blogs = parse_rss_feed(rss_content)
print(f"   ✓ Parsed {len(new_blogs)} entries from TechCrunch RSS feed")
print(f"   ✓ Sample titles:")
for i, blog in enumerate(new_blogs[:3], 1):
    print(f"      {i}. {blog['title']}")

# Step 4: Show data transformation
print("\n4. Data Transformation Details:")
sample = new_blogs[0]
print(f"   ✓ Title: {sample['title']}")
print(f"   ✓ Author: {sample['author']}")
print(f"   ✓ Category: {sample['category']}")
print(f"   ✓ Tags: {', '.join(sample['tags'][:3])}")
print(f"   ✓ Publish Date: {sample['publishDate']}")
print(f"   ✓ SEO Meta Title: {sample['seo']['metaTitle']}")
print(f"   ✓ Featured: {sample['featured']}")

# Step 5: Create temporary integration
print("\n5. Creating temporary integration demonstration...")
shutil.copy('blogs.json', 'blogs.json.demo.backup')

try:
    # Update blogs.json
    process_rss_feed(rss_content, 'blogs.json', update_file=True)
    
    # Show results
    with open('blogs.json', 'r') as f:
        updated = json.load(f)
        updated_count = len(updated['blogs'])
    
    print(f"   ✓ Integration complete!")
    print(f"   ✓ Total blogs after integration: {updated_count}")
    print(f"   ✓ New first blog: {updated['blogs'][0]['title']}")
    print(f"   ✓ Source: TechCrunch RSS Feed")
    
    # Show merged structure
    print("\n6. Merged Blog Structure:")
    if updated_count > 0:
        techcrunch_end_idx = min(7, updated_count - 1)
        print(f"   ├─ TechCrunch blogs (IDs: {updated['blogs'][0]['id']}-{updated['blogs'][techcrunch_end_idx]['id']})")
        if updated_count > 8:
            print(f"   └─ Original blogs (IDs: {updated['blogs'][8]['id']}-{updated['blogs'][-1]['id']})")
        else:
            print(f"   └─ Original blogs included in total count")
    
finally:
    # Restore original
    shutil.move('blogs.json.demo.backup', 'blogs.json')
    print("\n7. Restored original blogs.json")

print("\n" + "=" * 70)
print("✓ Demo Complete!")
print("=" * 70)
print("\nKey Features Demonstrated:")
print("  • RSS feed parsing and XML processing")
print("  • Automatic data transformation to portfolio format")
print("  • Category detection from tags")
print("  • SEO metadata generation")
print("  • Blog merging with ID management")
print("  • Integration with existing blog data")
print("\nTo use with real TechCrunch feed:")
print("  curl -o techcrunch.xml https://techcrunch.com/feed/")
print("  python3 rss_feed_processor.py techcrunch.xml --update")
