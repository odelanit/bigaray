import json

import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Joe-fresh_2_1'  # name_gender_type
    allowed_domains = ['www.joefresh.com']
    root_url = 'https://www.joefresh.com/ca'
    start_urls = [
        'https://www.joefresh.com/ca/**/c/20008/plpData?q=:relevance&sort=newest&page=0&t=1602662637536',
        'https://www.joefresh.com/ca/**/c/20008/plpData?q=:relevance&sort=newest&page=1&t=1602662637536',
    ]

    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)
        result = json_response[0]
        products = result['results']
        for product in products:
            item = ProductItem()
            item['title'] = product.get('name')
            item['price'] = product.get('minEffectivePrice').get('currencyIso') + product.get('minEffectivePrice').get('formattedValue')
            images = product.get('images')
            item['image_urls'] = [
                images.get('hover')[0],
                images.get('hover')[0]
            ]

            item['product_link'] = self.root_url + product.get('url')
            yield item
