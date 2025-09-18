import scrapy
from rssible.items import FeedItem
from datetime import datetime
import re

class GebaeudeforumSpider(scrapy.Spider):
    """
    Spider for German building forum (Gebäudeforum) news archive
    Scrapes building industry news, sustainability topics, and energy efficiency articles
    """
    name = 'gebaeudeforum'
    allowed_domains = ['gebaeudeforum.de']
    start_urls = ['https://www.gebaeudeforum.de/service/archiv-meldungen']

    def parse(self, response):
        # Extract language from HTML lang attribute
        page_language = response.xpath('//html/@lang').get()
        if not page_language:
            page_language = 'de-DE'  # Fallback for German content

        # Find the main article container
        article_container = response.css('#article')

        if not article_container:
            self.logger.warning("No article container found")
            return

        # Extract all teaser cards within the article
        teaser_cards = article_container.css('.c-teaser--card')

        self.logger.info(f"Found {len(teaser_cards)} teaser cards")

        for card in teaser_cards:
            # Extract title from h3.c-teaser__headline
            title = card.css('h3.c-teaser__headline::text').get()
            if not title:
                continue

            title = title.strip()

            # Extract description from the p element after the headline
            description = card.css('h3.c-teaser__headline + p::text').get()
            if not description:
                # Fallback: try to get any p text within the card
                description = card.css('p::text').get()

            if not description:
                description = title  # Use title as fallback
            else:
                description = description.strip()

            # Extract link from .c-teaser__link
            link = card.css('.c-teaser__link::attr(href)').get()
            if not link:
                continue

            # Extract date from span.c-kicker (format might be "Category | Date")
            kicker_text = card.css('span.c-kicker::text').get()
            pub_date = None

            if kicker_text:
                # Split by | and try to find the date part
                parts = kicker_text.split('|')
                for part in parts:
                    part = part.strip()
                    # Look for German date format (DD.MM.YYYY)
                    date_match = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', part)
                    if date_match:
                        try:
                            # Convert German date format to RSS date format
                            date_str = date_match.group(1)
                            date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                            pub_date = date_obj.strftime('%a, %d %b %Y %H:%M:%S +0000')
                            break
                        except ValueError:
                            continue

            # If no date found, use current time
            if not pub_date:
                pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

            # Create and yield the item
            item = FeedItem()
            item['title'] = title
            item['link'] = response.urljoin(link)
            item['description'] = f"Gebäudeforum: {description}"
            item['pub_date'] = pub_date
            item['source_url'] = response.url
            item['language'] = page_language

            self.logger.info(f"Extracted item: {title}")
            yield item
