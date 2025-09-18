#!/bin/bash

# Script to run a specific spider in Docker
# Usage: ./run-spider.sh <spider_name>
# Example: ./run-spider.sh hackernews

if [ $# -eq 0 ]; then
    echo "Usage: $0 <spider_name>"
    echo "Available spiders:"
    docker run --rm -v "$(pwd)/feeds:/app/feeds" rssible scrapy list
    exit 1
fi

SPIDER_NAME=$1

if [ "$SPIDER_NAME" = "list" ]; then
    echo "Available spiders:"
    docker run --rm -v "$(pwd)/feeds:/app/feeds" rssible scrapy list
    exit 0
fi

echo "Running spider: $SPIDER_NAME"
echo "Feeds will be saved to: $(pwd)/feeds/"

# Create feeds directory if it doesn't exist
mkdir -p feeds

# Run the spider
docker run --rm \
    -v "$(pwd)/feeds:/app/feeds" \
    rssible \
    scrapy crawl "$SPIDER_NAME"

echo "Spider completed! Check feeds/$SPIDER_NAME.xml for the generated RSS feed."
