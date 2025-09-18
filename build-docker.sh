#!/bin/bash

# Build the Docker image
echo "Building RSSible Docker image..."
docker build -t rssible .

echo "Docker image built successfully!"
echo ""
echo "Usage examples:"
echo "  Run single spider:    ./run-spider.sh hackernews"
echo "  Run all spiders:      ./run-all-spiders.sh"
echo "  List available:       ./run-spider.sh list"
