import scrapy
import logging

class DesktopSpider(scrapy.Spider):
    name = 'desktop'
    allowed_domains = ['www.yodobashi.com']
    start_urls = ['http://www.yodobashi.com/category/19531/11970/34646/']

    def parse(self, response):
        logging.info(response.request.headers['User-Agent']) # user-agentの取得
        logging.info(response.url)
        products = response.xpath('//div[contains(@class,"productListTile")]')
        # products = response.css('div.productListTile')
        for product in products:
            maker = product.xpath('.//div[contains(@class,"pName")]/p/text()').get()
            # maker = product.css('div.pName > p::text')
            name = product.xpath('.//div[contains(@class,"pName")]/p[2]/text()').get()
            price = product.xpath('.//span[@class="productPrice"]/text()').get()
            yield {
                'maker': maker,
                'name': name,
                'price': price
            }
        next_page = response.xpath('//a[@class="next"]/@href').get()
        if next_page:
            yield response.follow(url=next_page, callback=self.parse)