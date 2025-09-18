# RSSible - Web Scraping to RSS Feed Generator

A simple Python + Scrapy project that scrapes multiple webpages and creates XML RSS feeds for each of them. Perfect for converting websites without RSS feeds into RSS-enabled sources.

## 🚀 Features

- **Easy to use**: Simple Python project structure, beginner-friendly
- **Multiple spiders**: Scrape different websites with individual spiders
- **Automated RSS generation**: Converts scraped content into proper XML RSS feeds
- **Docker support**: Run everything in containers for consistent environments
- **GitHub Actions integration**: Automatically runs scraping and updates feeds on schedule
- **Configurable**: Easy to add new websites to scrape

## 📁 Project Structure

```
rssible/
├── rssible/              # Main Scrapy project
│   ├── spiders/          # Individual website scrapers
│   ├── items.py          # Data structure definitions
│   ├── pipelines.py      # RSS XML generation logic
│   └── settings.py       # Scrapy configuration
├── feeds/                # Generated RSS XML files
├── .github/workflows/    # GitHub Actions automation
├── Dockerfile            # Docker container configuration
├── compose.yml           # Docker Compose setup
├── build-docker.sh       # Build Docker image script
├── run-spider.sh         # Run single spider script
├── run-all-spiders.sh    # Run all spiders script
├── requirements.txt      # Python dependencies
└── scrapy.cfg           # Scrapy project configuration
```

## 🛠️ Setup

### Prerequisites
- Docker and Docker Compose (recommended)
- OR Python 3.8+ and pip (for local development)
- Git

### Docker Setup (Recommended)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rssible
   ```

2. **Build Docker image**
   ```bash
   ./build-docker.sh
   ```

3. **Run a single spider**
   ```bash
   # Run Hacker News spider
   ./run-spider.sh hackernews

   # Run TechCrunch spider
   ./run-spider.sh techcrunch

   # Run Gebäudeforum spider (German building industry news)
   ./run-spider.sh gebaeudeforum

   # List available spiders
   ./run-spider.sh list
   ```

4. **Run all spiders at once**
   ```bash
   ./run-all-spiders.sh
   ```

5. **Using Docker Compose**
   ```bash
   # Run specific spider
   docker-compose run --rm rssible scrapy crawl gebaeudeforum
   ```

### Local Development (Alternative)

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rssible
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Test a spider**
   ```bash
   # Run the Gebäudeforum spider
   scrapy crawl gebaeudeforum
   ```

4. **Check generated feeds**
   ```bash
   ls feeds/
   # You should see: hackernews.xml, techcrunch.xml
   ```

## 🕷️ Creating New Spiders

To scrape a new website, create a new spider file in `rssible/spiders/`:

```python
import scrapy
from rssible.items import FeedItem
from datetime import datetime

class YourSiteSpider(scrapy.Spider):
    name = 'yoursite'  # This will be the feed filename: yoursite.xml
    allowed_domains = ['yoursite.com']
    start_urls = ['https://yoursite.com/']

    def parse(self, response):
        # Extract articles/posts from the page
        articles = response.css('article')  # Adjust CSS selector

        for article in articles[:10]:  # Limit to 10 items
            title = article.css('h2 a::text').get()  # Adjust selector
            link = article.css('h2 a::attr(href)').get()  # Adjust selector
            description = article.css('p::text').get()  # Adjust selector

            if title and link:
                item = FeedItem()
                item['title'] = title.strip()
                item['link'] = response.urljoin(link)
                item['description'] = description.strip() if description else title.strip()
                item['pub_date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                item['source_url'] = response.url

                yield item
```

### Key points for new spiders:
- **Name**: The `name` field determines the output XML filename
- **CSS Selectors**: Adjust the CSS selectors to match the target website's HTML structure
- **Allowed Domains**: Add the website's domain to `allowed_domains`
- **Start URLs**: Add the page(s) you want to scrape to `start_urls`

## ⚙️ GitHub Actions Automation

The project includes automated RSS feed generation using GitHub Actions with Docker:

- **Schedule**: Runs every 6 hours automatically
- **Docker-based**: Uses Docker for consistent environments across runs
- **Manual trigger**: Can be triggered manually from GitHub Actions tab
- **Auto-commit**: Automatically commits updated RSS feeds back to the repository

### To enable automation:

1. Push your code to GitHub
2. The workflow will run automatically based on the schedule
3. Generated RSS feeds will be available in the `feeds/` directory
4. Access feeds via: `https://raw.githubusercontent.com/yourusername/rssible/main/feeds/hackernews.xml`

## 🔧 Configuration

### Adding spiders to GitHub Actions

Edit `.github/workflows/generate-feeds.yml` and add your new spider:

```yaml
- name: Run your new spider
  run: |
    docker run --rm -v "${{ github.workspace }}/feeds:/app/feeds" rssible scrapy crawl yournewspider
```

### Scrapy Settings

Key settings in `rssible/settings.py`:

- `DOWNLOAD_DELAY`: Time between requests (be respectful!)
- `ROBOTSTXT_OBEY`: Whether to respect robots.txt (recommended: True)
- `CONCURRENT_REQUESTS`: Number of simultaneous requests

## 📊 RSS Feed Format

Generated feeds follow standard RSS 2.0 format:

```xml
<?xml version='1.0' encoding='utf-8'?>
<rss version="2.0">
  <channel>
    <title>RSS Feed - spidername</title>
    <description>Automatically generated RSS feed from spidername spider</description>
    <language>en-us</language>
    <lastBuildDate>Wed, 18 Sep 2025 10:30:00 +0000</lastBuildDate>
    <item>
      <title>Article Title</title>
      <link>https://example.com/article</link>
      <description>Article description</description>
      <pubDate>Wed, 18 Sep 2025 10:30:00 +0000</pubDate>
      <guid>https://example.com/article</guid>
    </item>
  </channel>
</rss>
```

## 🚨 Best Practices

1. **Be respectful**: Don't overwhelm websites with requests
2. **Check robots.txt**: Always respect website scraping policies
3. **Use delays**: Configure appropriate delays between requests
4. **Monitor feeds**: Check that your spiders work correctly
5. **Handle errors**: Test your CSS selectors thoroughly

## 🐛 Troubleshooting

### Common Issues

**Spider not finding content**:
- Check CSS selectors using browser developer tools
- Website might have changed its HTML structure

**Empty feeds**:
- Verify the website allows scraping (check robots.txt)
- CSS selectors might be incorrect
- Website might be using JavaScript (Scrapy only handles static HTML)

**Docker issues**:
- Make sure Docker is installed and running
- Check that the `feeds/` directory has proper permissions
- Try rebuilding the Docker image: `./build-docker.sh`

**GitHub Actions failing**:
- Check that all spider names in the workflow file are correct
- Verify Docker build succeeds locally first

## 📝 Example Usage

### With Docker (Recommended)
1. Build: `./build-docker.sh`
2. Run single spider: `./run-spider.sh hackernews`
3. Run all spiders: `./run-all-spiders.sh`
4. Check feeds: `ls feeds/`

### For GitHub Actions
1. Add your spiders for the websites you want to monitor
2. Push to GitHub to enable automation
3. Subscribe to the generated RSS feeds in your preferred RSS reader
4. Feeds update automatically every 6 hours

## 🤝 Contributing

1. Fork the repository
2. Create a new spider for a website
3. Test it locally
4. Submit a pull request

## 📄 License

This project is open source. Feel free to use and modify as needed.
