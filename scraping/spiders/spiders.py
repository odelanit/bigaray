from shutil import which

import scrapy
from scrapy_selenium import SeleniumRequest

from backend.models import Product
from scraping.spiders.items import ProductItem


class BrokenLinksSpider(scrapy.Spider):
    name = 'brokenlink-checker'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1,
        'SELENIUM_DRIVER_NAME': 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': which('geckodriver'),
        # 'SELENIUM_DRIVER_ARGUMENTS': ['-headless'],
        'SELENIUM_DRIVER_ARGUMENTS': [],
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_selenium.SeleniumMiddleware': 800,
        },
        'ITEM_PIPELINES': {
            'scraping.spiders.pipelines.ProductUpdatePipeline': 300,
        }
    }

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.start_urls = []
        products = Product.objects.all()
        for product in products:
            self.start_urls.append(product.product_link)

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    def parse(self, response, **kwargs):
        item = ProductItem()
        item['product_link'] = response.request.url
        item['status'] = response.status
        yield item
