import scrapy
from scrapy.crawler import CrawlerProcess

class HeraldSpider(scrapy.Spider):
    name = "herald"
    start_urls = ['https://www.herald.co.zw/category/articles/top-stories/']

    def parse(self, response):
        articles = response.css('h3 a')
        for article in articles:
            title = article.css('::text').get().strip()
            link = article.css('::attr(href)').get()
            yield response.follow(link, callback=self.parse_article, meta={'title': title})

    def parse_article(self, response):
        content_section = response.css('div.post--content')
        content = content_section.css('::text').getall() if content_section else "No content found"
        yield {
            'Category': 'Top Stories',
            'Content': ' '.join(content).strip(),
            'Link': response.url,
            'Source': 'The Herald',
            'Title': response.meta['title']
        }

def main():
    process = CrawlerProcess(settings={
        'FEEDS': {
            'herald_news_articles.csv': {'format': 'csv', 'overwrite': True},
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    })

    process.crawl(HeraldSpider)
    process.start()

if __name__ == "__main__":
    main()
