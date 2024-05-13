import scrapy
from scrapy.crawler import CrawlerProcess
from ..items import ScrapenewsItem

class ScrapeNews(scrapy.Spider):
    name = 'news_bbc'
    start_urls = [
        #'https://www.bbc.com/news/us-canada' # this is politics 
        #'https://www.bbc.com/culture'
        'https://www.bbc.com/business'
        #'https://www.bbc.com/sports' #problem here
    ]

    def parse(self, response):
        if 'us-canada' in response.url:
            category = 'politics'
        else:
            category = response.url.split('/')[-1]

        all_news = response.css(".khCtOO")

        for news in all_news:
            loader = ItemLoader(item=ScrapenewsItem(), selector=news)

            loader.add_css('title', '.bvDsJq::text')
            loader.add_css('content', '.cNPpME::text')
            loader.add_value('category', category)
            loader.add_value('source', 'BBC')

            relative_link = news.css('div[data-testid="edinburgh-card"] a[data-testid="internal-link"]::attr(href)').get()
            link = response.urljoin(relative_link)
            loader.add_value('link', link)

            yield loader.load_item()

def start_spider():
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    })
    process.crawl(ScrapeNews)
    process.start()

if __name__ == "__main__":
    start_spider()
