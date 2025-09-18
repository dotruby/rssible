import scrapy
from rssible.items import FeedItem
from datetime import datetime

class HackerNewsSpider(scrapy.Spider):
    """
    Example spider that scrapes Hacker News front page
    This demonstrates how to create a simple spider for RSS generation
    """
    name = 'hackernews'
    allowed_domains = ['news.ycombinator.com']
    start_urls = ['https://news.ycombinator.com/']

    def parse(self, response):
        # Extract story links and titles
        stories = response.css('tr.athing')
        
        for story in stories[:10]:  # Limit to first 10 stories
            title_link = story.css('span.titleline > a::attr(href)').get()
            title_text = story.css('span.titleline > a::text').get()
            
            if title_text and title_link:
                # Create feed item
                item = FeedItem()
                item['title'] = title_text.strip()
                
                # Handle relative URLs
                if title_link.startswith('item?'):
                    item['link'] = response.urljoin(title_link)
                elif title_link.startswith('http'):
                    item['link'] = title_link
                else:
                    item['link'] = response.urljoin(title_link)
                
                item['description'] = f"Story from Hacker News: {title_text.strip()}"
                item['pub_date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                item['source_url'] = response.url
                
                yield item
