import os
import xml.etree.ElementTree as ET
from datetime import datetime
from scrapy.exceptions import DropItem

class XMLFeedPipeline:
    """
    Pipeline to generate XML/RSS feeds from scraped items
    """

    def __init__(self):
        self.feeds = {}
        self.languages = {}

    def open_spider(self, spider):
        """Initialize feed for this spider"""
        self.feeds[spider.name] = []

    def close_spider(self, spider):
        """Generate XML feed when spider closes"""
        if spider.name in self.feeds and self.feeds[spider.name]:
            self.generate_xml_feed(spider.name, self.feeds[spider.name])

    def process_item(self, item, spider):
        """Process each scraped item"""
        if not item.get('title') or not item.get('link'):
            raise DropItem(f"Missing title or link in {item}")

        # Add current timestamp if pub_date is missing
        if not item.get('pub_date'):
            item['pub_date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

        # Generate GUID if missing
        if not item.get('guid'):
            item['guid'] = item['link']

        # Store spider name
        item['spider_name'] = spider.name

        # Store language for this spider (use first detected language)
        if item.get('language') and spider.name not in self.languages:
            self.languages[spider.name] = item['language']

        self.feeds[spider.name].append(dict(item))
        return item

    def generate_xml_feed(self, spider_name, items):
        """Generate RSS XML feed"""
        # Create RSS root element
        rss = ET.Element('rss', version='2.0')
        channel = ET.SubElement(rss, 'channel')

        # Use detected language or fallback to English
        language = self.languages.get(spider_name, 'en-us')

        # Channel information
        ET.SubElement(channel, 'title').text = f'RSS Feed - {spider_name}'
        ET.SubElement(channel, 'description').text = f'Automatically generated RSS feed from {spider_name} spider'
        ET.SubElement(channel, 'language').text = language
        ET.SubElement(channel, 'lastBuildDate').text = datetime.now().strftime('%a, %d %b %Y %H:%M:%S %z')

        # Add items
        for item in items:
            item_elem = ET.SubElement(channel, 'item')
            ET.SubElement(item_elem, 'title').text = item.get('title', '')
            ET.SubElement(item_elem, 'link').text = item.get('link', '')
            ET.SubElement(item_elem, 'description').text = item.get('description', '')
            ET.SubElement(item_elem, 'pubDate').text = item.get('pub_date', '')
            ET.SubElement(item_elem, 'guid').text = item.get('guid', '')

        # Write to file
        os.makedirs('feeds', exist_ok=True)
        tree = ET.ElementTree(rss)
        ET.indent(tree, space="  ", level=0)

        # Write XML with proper double quotes in declaration
        xml_content = ET.tostring(rss, encoding='utf-8', xml_declaration=False).decode('utf-8')
        xml_declaration = '<?xml version="1.0" encoding="utf-8"?>\n'

        with open(f'feeds/{spider_name}.xml', 'w', encoding='utf-8') as f:
            f.write(xml_declaration + xml_content)
