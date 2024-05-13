import scrapy
from scrapy.crawler import CrawlerProcess

class NBCBusinessSpider(scrapy.Spider):
    name = "nbc_business"
    start_urls = ['https://www.nbcnews.com/business']

    def parse(self, response):
        for div in response.css("div.wide-tease-item__info-wrapper"):
            links = div.css('a')
            if len(links) > 1:
                news = links[1]
                title = news.css('h2::text').get().strip() if news.css('h2::text').get() else "No title found"
                relative_link = news.css('::attr(href)').get()
                full_link = response.urljoin(relative_link)
                yield scrapy.Request(full_link, callback=self.parse_article, meta={'title': title})

    def parse_article(self, response):
        content = ' '.join([p.css('::text').get().strip() for p in response.css('div.article-body__content p')])
        yield {
            'Category': 'business',
            'Content': content,
            'Link': response.url,
            'Source': 'NBC',
            'Title': response.meta['title']
        }

def main():
    process = CrawlerProcess(settings={
        'FEEDS': {
            'nbcnews_business_data.csv': {'format': 'csv', 'overwrite': True},
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
    })

    process.crawl(NBCBusinessSpider)
    process.start()

if __name__ == "__main__":
    main()
