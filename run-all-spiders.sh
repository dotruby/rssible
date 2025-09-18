#!/bin/bash

# Script to run all spiders using docker-compose
echo "Running all RSSible spiders..."
echo "This will generate RSS feeds for all configured websites."
echo ""

# Create feeds directory if it doesn't exist
mkdir -p feeds

# Run all spiders using docker-compose
docker-compose up --build rssible-all

echo ""
echo "All spiders completed!"
echo "Generated RSS feeds:"
ls -la feeds/*.xml 2>/dev/null || echo "No XML feeds found. Check for errors above."
