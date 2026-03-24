#!/bin/bash

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Testing New RSS Feeds for Quality Content"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Test each feed and extract the first 3 article titles
declare -a feeds=(
    "https://stackoverflow.blog/feed/"
    "https://www.freecodecamp.org/news/rss/"
    "https://dev.to/feed"
    "https://machinelearningmastery.com/feed/"
)

declare -a feed_names=(
    "Stack Overflow Blog"
    "FreeCodeCamp"
    "Dev.to"
    "Machine Learning Mastery"
)

for i in "${!feeds[@]}"; do
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "📰 ${feed_names[$i]}"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Feed URL: ${feeds[$i]}"
    echo ""
    echo "Latest Articles:"

    # Fetch feed and extract titles
    curl -s "${feeds[$i]}" | grep -oP '(?<=<title>).*?(?=</title>)' | sed 's/<!\[CDATA\[//g' | sed 's/\]\]>//g' | head -4 | tail -3 | nl

    echo ""
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Test Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "These feeds provide:"
echo "  ✓ Programming tutorials and best practices"
echo "  ✓ AI/ML development guides"
echo "  ✓ Web development techniques"
echo "  ✓ Software engineering insights"
echo ""
echo "Much better than TechCrunch business news!"
echo ""
