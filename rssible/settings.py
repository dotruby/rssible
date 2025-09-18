# Scrapy settings for rssible project

BOT_NAME = 'rssible'

SPIDER_MODULES = ['rssible.spiders']
NEWSPIDER_MODULE = 'rssible.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure a delay for requests (be respectful)
DOWNLOAD_DELAY = 1
RANDOMIZE_DOWNLOAD_DELAY = True

# Configure pipelines
ITEM_PIPELINES = {
    'rssible.pipelines.XMLFeedPipeline': 300,
}

# User agent
USER_AGENT = 'rssible (+http://www.yourdomain.com)'

# Configure maximum concurrent requests
CONCURRENT_REQUESTS = 16
CONCURRENT_REQUESTS_PER_DOMAIN = 8

# Enable autothrottling
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 1
AUTOTHROTTLE_MAX_DELAY = 60
AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0

# Log level
LOG_LEVEL = 'INFO'

# Feeds output directory
FEEDS_STORE = 'feeds/'
