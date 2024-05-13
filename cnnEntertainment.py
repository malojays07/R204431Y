import scrapy
from scrapy.crawler import CrawlerProcess

class CNNEntertainmentSpider(scrapy.Spider):
    name = "cnn_entertainment"
    start_urls = ['https://edition.cnn.com/entertainment']

    def parse(self, response):
        for news in response.css("div.container_lead-plus-headlines-with-images__item.container_lead-plus-headlines-with-images__item--type-section a"):
            title = news.css('span::text').get().strip() if news.css('span::text').get() else "No title found"
            relative_link = news.css('::attr(href)').get()
            full_link = response.urljoin(relative_link)
            yield scrapy.Request(full_link, callback=self.parse_article, meta={'title': title})

    def parse_article(self, response):
        content = ' '.join([p.css('::text').get().strip() for p in response.css('div.article__content p.paragraph.inline-placeholder.vossi-paragraph-primary-core-light')])
        yield {
            'Category': 'Entertainment',
            'Content': content,
            'Link': response.url,
            'Source': 'CNN',
            'Title': response.meta['title']
        }

def main():
    process = CrawlerProcess(settings={
        'FEEDS': {
            'cnn_entertainment.csv': {'format': 'csv', 'overwrite': True},
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    })

    process.crawl(CNNEntertainmentSpider)
    process.start()

if __name__ == "__main__":
    main()
