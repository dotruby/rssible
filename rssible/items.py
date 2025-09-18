import scrapy
from datetime import datetime

class FeedItem(scrapy.Item):
    """
    Item class for RSS feed entries
    """
    title = scrapy.Field()
    link = scrapy.Field()
    description = scrapy.Field()
    pub_date = scrapy.Field()
    guid = scrapy.Field()
    source_url = scrapy.Field()
    spider_name = scrapy.Field()
    language = scrapy.Field()
