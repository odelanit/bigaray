import scrapy

from backend.models import Product


class AbilitySpider(scrapy.Spider):
    name = 'check_products'
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'DOWNLOAD_DELAY': 1
    }

    def __init__(self, name=None, **kwargs):
        self.start_urls = []
        products = Product.objects.all()
        for product in products:
            self.start_urls.append(product.product_link)
        super().__init__(name, **kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url=url)

    def parse(self, response, **kwargs):
        pass
