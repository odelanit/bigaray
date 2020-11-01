from shutil import which

import scrapy
from scrapy_selenium import SeleniumRequest

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Old-navy_2_1'  # name_gender_type
    allowed_domains = ['oldnavy.gapcanada.ca']
    start_urls = [
        'https://oldnavy.gapcanada.ca/browse/category.do?cid=11174'
    ]
    custom_settings = {
        'SELENIUM_DRIVER_NAME': 'firefox',
        'SELENIUM_DRIVER_EXECUTABLE_PATH': which('geckodriver'),
        # 'SELENIUM_DRIVER_ARGUMENTS': ['-headless'],
        'SELENIUM_DRIVER_ARGUMENTS': [],
        'SELENIUM_PROXY': '46.250.220.148:3128',
        'DOWNLOADER_MIDDLEWARES': {
            'scraping.spiders.middlewares.SeleniumMiddleware': 800,
        },
        'ITEM_PIPELINES': {
            'scraping.spiders.pipelines.ProductPipeline': 300,
            'scraping.spiders.pipelines.ImagesWithSeleniumProxyPipeline': 2,
        }
    }

    def start_requests(self):
        for url in self.start_urls:
            yield SeleniumRequest(url=url)

    def parse(self, response, **kwargs):
        products = response.css('.product-card')
        for product in products:
            title = product.css('.product-card__name::text').get()
            highlight_price = product.css('.product-price__highlight::text').get()
            price = product.css('.product-card-price > div:first-child > span > span::text').get()
            image_url = product.css('img::attr(src)').get()
            product_link = product.css('.product-card__link::attr(href)').get()

            print("title: {0}".format(title))
            print("price: {0}".format(price))
            print("highlight: {0}".format(highlight_price))
            print("image_url: {0}".format(image_url))
            print("product_link: {0}".format(product_link))

            if title and (highlight_price or price) and image_url and product_link:
                item = ProductItem()
                item['title'] = title
                if price:
                    item['price'] = price
                else:
                    item['price'] = highlight_price
                item['image_urls'] = [image_url, image_url]
                item['product_link'] = product_link
                yield item
