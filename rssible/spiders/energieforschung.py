import scrapy
from rssible.items import FeedItem
from datetime import datetime
import re

class EnergiforschungSpider(scrapy.Spider):
    """
    Spider for German energy research news (Energieforschung.de)
    Scrapes energy research news, sustainability topics, and renewable energy articles
    """
    name = 'energieforschung'
    allowed_domains = ['energieforschung.de']
    start_urls = ['https://www.energieforschung.de/de/aktuelles/neuigkeiten']

    def parse(self, response):
        # Extract language from HTML lang attribute
        page_language = response.xpath('//html/@lang').get()
        if not page_language:
            page_language = 'de-DE'  # Fallback for German content

        # Find all p.subline elements which contain the date information
        subline_elements = response.css('p.subline')

        self.logger.info(f"Found {len(subline_elements)} subline elements")

        for subline in subline_elements:
            # Get the parent element of p.subline
            parent = subline.xpath('./..').get()
            if not parent:
                continue

            # Create a selector for the parent element
            parent_selector = scrapy.Selector(text=parent)

            # Extract date from span.date within the subline
            date_span = subline.css('span.date::text').get()
            pub_date = None

            if date_span:
                date_span = date_span.strip()
                # Look for German date format (DD.MM.YYYY or similar)
                date_match = re.search(r'(\d{1,2}\.\d{1,2}\.\d{4})', date_span)
                if date_match:
                    try:
                        # Convert German date format to RSS date format
                        date_str = date_match.group(1)
                        date_obj = datetime.strptime(date_str, '%d.%m.%Y')
                        pub_date = date_obj.strftime('%a, %d %b %Y %H:%M:%S +0000')
                    except ValueError:
                        pass

            # If no date found, use current time
            if not pub_date:
                pub_date = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')

            # Extract headline and link from headline-link in the parent
            headline_link = parent_selector.css('.headline-link')
            if not headline_link:
                continue

            # Get the href attribute
            link = headline_link.css('::attr(href)').get()
            if not link:
                continue

            # Get the headline text from h3 within the headline-link
            title = headline_link.css('h3::text').get()
            if not title:
                # Fallback: try to get any text within the link
                title = headline_link.css('::text').get()

            if not title:
                continue

            title = title.strip()

            # Extract description from the p element that follows the headline-link
            # Find the headline-link element and then get the next p sibling
            description_p = parent_selector.css('.headline-link + p::text').get()
            if not description_p:
                # Fallback: try to find any p element after the headline-link
                description_p = parent_selector.css('.headline-link ~ p::text').get()

            if not description_p:
                description = title  # Use title as fallback
            else:
                description = description_p.strip()

            # Create and yield the item
            item = FeedItem()
            item['title'] = title
            item['link'] = response.urljoin(link)
            item['description'] = description
            item['pub_date'] = pub_date
            item['source_url'] = response.url
            item['language'] = page_language

            self.logger.info(f"Extracted item: {title}")
            yield item
