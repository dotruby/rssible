import scrapy


class BaseSpider(scrapy.Spider):
    """
    Base spider class with common functionality for all spiders
    """

    def __init__(self, max_items=None, *args, **kwargs):
        super(BaseSpider, self).__init__(*args, **kwargs)
        self.max_items = int(max_items) if max_items else None
        self.items_count = 0
        if self.max_items:
            self.logger.info(f"Max items limit set to: {self.max_items}")

    def should_continue_scraping(self):
        """Check if we should continue scraping based on max_items limit"""
        if self.max_items and self.items_count >= self.max_items:
            self.logger.info(f"Reached max_items limit of {self.max_items}")
            return False
        return True

    def increment_items_count(self):
        """Increment the items counter"""
        self.items_count += 1
