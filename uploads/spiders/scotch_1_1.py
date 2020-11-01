import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Scotch-soda_1_1'  # name_gender_type
    allowed_domains = ['www.scotch-soda.com']
    start_urls = [
        'https://www.scotch-soda.com/ca/en/women/new-arrivals?sz=120',
    ]

    def parse(self, response, **kwargs):
        products = response.css('div.product-tile')
        for idx, product in enumerate(products):
            item = ProductItem()
            item['title'] = product.css('.product__name::text').get().strip()
            item['price'] = product.css('.product__price::text').get().strip()
            image_url = product.css('img::attr(data-src)').get()
            item['image_urls'] = [image_url, image_url]
            item['product_link'] = product.css('a::attr(href)').get()
            yield item

