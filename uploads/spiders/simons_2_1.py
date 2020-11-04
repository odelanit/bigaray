from shutil import which

import scrapy
from scrapy_selenium import SeleniumRequest

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Simons_2_1'  # name_gender_type
    allowed_domains = ['www.simons.ca']
    start_urls = [
        'https://www.simons.ca/fr/vetements-homme/nouveautes--new-6714?page=%s' % page for page in range(1, 12)
    ]
    base_url = 'https://www.simons.ca'
    custom_settings = {
        'SELENIUM_DRIVER_NAME': 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': which('geckodriver'),
        'SELENIUM_DRIVER_ARGUMENTS': ['-headless'],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    def parse(self, response, **kwargs):
        products = response.css('div.product_card')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('span[itemprop="name"]::text').get()
            price = product.css('span.salePrice::text').get().strip()
            item['price'] = price
            image_url = product.css('img::attr(src)').get()
            item['image_urls'] = [image_url, image_url]
            item['product_link'] = product.css('a.desc::attr(href)').get()
            yield item

