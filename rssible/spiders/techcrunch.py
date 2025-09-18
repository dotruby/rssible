import scrapy
from rssible.items import FeedItem
from datetime import datetime

class TechCrunchSpider(scrapy.Spider):
    """
    Example spider that scrapes TechCrunch latest articles
    """
    name = 'techcrunch'
    allowed_domains = ['techcrunch.com']
    start_urls = ['https://techcrunch.com/']

    def parse(self, response):
        # Extract article links from TechCrunch homepage
        articles = response.css('article.post-block')
        
        for article in articles[:10]:  # Limit to first 10 articles
            title = article.css('h2.post-block__title a::text').get()
            link = article.css('h2.post-block__title a::attr(href)').get()
            description = article.css('div.post-block__content::text').get()
            
            if title and link:
                item = FeedItem()
                item['title'] = title.strip()
                item['link'] = response.urljoin(link)
                item['description'] = description.strip() if description else f"Article from TechCrunch: {title.strip()}"
                item['pub_date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                item['source_url'] = response.url
                
                yield item
