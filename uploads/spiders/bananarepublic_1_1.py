from shutil import which

import scrapy
from scrapy_selenium import SeleniumRequest

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Banana-republic_1_1'  # name_gender_type
    allowed_domains = ['bananarepublic.gapcanada.ca']
    start_urls = [
        'https://bananarepublic.gapcanada.ca/browse/category.do?cid=48422',
        'https://bananarepublic.gapcanada.ca/browse/category.do?cid=48422#pageId=1&department=136'
    ]

    custom_settings = {
        'SELENIUM_DRIVER_NAME': 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': which('geckodriver'),
        'SELENIUM_DRIVER_ARGUMENTS': ['-headless'],
        # 'SELENIUM_DRIVER_ARGUMENTS': [],
        # 'SELENIUM_PROXY': '46.250.220.148:3128',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy_app.middlewares.SeleniumMiddleware': 800,
        },
        'ITEM_PIPELINES': {
            'scrapy_app.pipelines.ProductPipeline': 300,
            'scrapy_app.pipelines.ImagesWithSeleniumProxyPipeline': 2,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    def parse(self, response, **kwargs):
        products = response.css('.product-card')
        for product in products:
            title = product.css('.product-card__name::text').get()
            price = product.css('span.product-price__no-strike::text').get()
            image_url = product.css('img::attr(src)').get()
            product_link = product.css('.product-card__link::attr(href)').get()

            if title and price and image_url and product_link:
                item = ProductItem()
                item['title'] = title
                item['price'] = price
                if image_url:
                    item['image_urls'] = [image_url, image_url]
                else:
                    continue
                item['product_link'] = product_link
                yield item
