import json

import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Joe-fresh_2_2'  # name_gender_type
    allowed_domains = ['www.joefresh.com']
    root_url = 'https://www.joefresh.com/ca'
    start_urls = [
        'https://www.joefresh.com/ca/**/c/20057/plpData?q=:relevance&sort=popular-desc&page=%s&t=1602662719047' % page for page in range(0, 1)
    ]

    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)
        result = json_response[0]
        products = result['results']
        for product in products:
            item = ProductItem()
            item['title'] = product.get('name')
            item['price'] = product.get('minEffectivePrice').get('currencyIso') + product.get('minEffectivePrice').get('formattedValue')
            if product.get('minRegularPrice'):
                item['sale_price'] = product.get('minRegularPrice').get('currencyIso') + product.get('minRegularPrice').get('formattedValue')
            images = product.get('images')
            item['image_urls'] = [
                images.get('hover')[0],
                images.get('hover')[0]
            ]

            item['product_link'] = self.root_url + product.get('url')
            yield item
