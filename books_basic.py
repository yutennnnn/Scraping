import scrapy
import logging

class BooksBasicSpider(scrapy.Spider):
    name = 'books_basic'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['https://books.toscrape.com/catalogue/category/books/fantasy_19/index.html']

    def parse(self, response):
        logging.info(response.request.headers['User-Agent'])
        logging.info(response.url)
        books = response.xpath('//h3')
        for book in books:
            title = book.xpath('.//a/@title').get()
            url = book.xpath('.//a/@href').get()
            yield {
                'title': title,
                'url': url
            }
        next_page = response.xpath('//li[@class="next"]/a/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)