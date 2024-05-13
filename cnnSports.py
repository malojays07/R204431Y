import scrapy
from scrapy.crawler import CrawlerProcess

class CNNSportsSpider(scrapy.Spider):
    name = "cnn_sports"
    start_urls = ['https://edition.cnn.com/sport']

    def parse(self, response):
        for div in response.css("div.container_lead-plus-headlines-with-images__item--type-section"):
            links = div.css('a')
            if len(links) > 1:
                news = links[1]
                title = news.css('span.container__headline-text::text').get().strip() if news.css('span.container__headline-text::text').get() else None
                relative_link = news.css('::attr(href)').get()
                full_link = response.urljoin(relative_link)
                yield scrapy.Request(full_link, callback=self.parse_article, meta={'title': title})

    def parse_article(self, response):
        content = ' '.join([p.css('::text').get().strip() for p in response.css('div.article__content p.paragraph.inline-placeholder.vossi-paragraph-primary-core-light')])
        yield {
            'Category': 'sport',
            'Content': content,
            'Link': response.url,
            'Source': 'CNN',
            'Title': response.meta['title']
        }

def main():
    process = CrawlerProcess(settings={
        'FEEDS': {
            'cnn_sports.csv': {'format': 'csv', 'overwrite': True},
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    })

    process.crawl(CNNSportsSpider)
    process.start()

if __name__ == "__main__":
    main()
