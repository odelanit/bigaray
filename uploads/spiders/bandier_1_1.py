import json

import scrapy

from scrapy_app.items import ProductItem


class ProductSpider(scrapy.Spider):
    name = 'Bandier_1_1'  # name_gender_type
    allowed_domains = ['www.bandier.com']
    start_urls = [
        'https://api.searchspring.net/api/search/search.json?siteId=96jhb3&bgfilter.collection_id=163934109730&&resultsFormat=native&page=%s' % page for page in range(1, 4)
    ]

    def parse(self, response, **kwargs):
        json_response = json.loads(response.body)
        products = json_response.get('results')
        for product in products:
            item = ProductItem()
            image_url = product.get('imageUrl')

            item['title'] = product.get('title')
            item['price'] = "${0}".format(product.get('price'))
            item['image_urls'] = [image_url, image_url]
            item['product_link'] = product.get('url')
            yield item
